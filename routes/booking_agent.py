from flask import Blueprint, render_template, session, redirect, url_for, abort, request
from db import get_db_connection

booking_agent_bp = Blueprint("booking_agent", __name__)

COMMISSION_RATE = 0.10


# ----------------------------
# Helper: only booking agents can access these pages
# ----------------------------
def require_booking_agent():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("user_type") != "booking_agent":
        abort(403)


# ----------------------------
# Helper: get the airline this booking agent is authorized to represent
# ----------------------------
def get_agent_airline(cursor, agent_email):
    cursor.execute("""
        SELECT airline_name
        FROM booking_agent
        WHERE agent_email = %s
    """, (agent_email,))
    row = cursor.fetchone()
    return row["airline_name"] if row else None


# ----------------------------
# Route: Booking Agent Home
# Shows the booking agent dashboard after login.
# ----------------------------
@booking_agent_bp.route("/booking_agent_home")
def booking_agent_home():
    check = require_booking_agent()
    if check:
        return check

    return render_template(
        "booking_agent_page/booking_agent_home.html",
        username=session.get("username")
    )


# ----------------------------
# Route: Booking Agent Flights
# Shows flights purchased by this booking agent.
# Supports filters for date range, origin, and destination.
# ----------------------------
@booking_agent_bp.route("/booking_agent_flights", methods=["GET", "POST"])
def booking_agent_flights():
    check = require_booking_agent()
    if check:
        return check

    agent_email = session.get("username")

    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    origin = request.form.get("origin", "").strip()
    destination = request.form.get("destination", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT airport_name, city
        FROM airport
        ORDER BY city, airport_name
    """)
    airports = cursor.fetchall()

    query = """
        SELECT
            bap.purchase_date,
            bap.ticket_id,
            cp.customer_email,
            mf.marketing_airline_name,
            mf.marketing_flight_num,
            ofl.operating_airline_name,
            ofl.flight_number AS operating_flight_num,
            ofl.departure_port,
            ofl.arrival_port,
            ofl.departure_time,
            ofl.arrival_time,
            ofl.price,
            ROUND(ofl.price * %s, 2) AS commission,
            ofl.status
        FROM booking_agent_purchases bap
        JOIN ticket t
            ON bap.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        LEFT JOIN customer_purchases cp
            ON bap.ticket_id = cp.ticket_id
        WHERE bap.agent_email = %s
    """

    params = [COMMISSION_RATE, agent_email]

    if start_date:
        query += " AND DATE(ofl.departure_time) >= %s"
        params.append(start_date)

    if end_date:
        query += " AND DATE(ofl.departure_time) <= %s"
        params.append(end_date)

    if origin:
        query += " AND ofl.departure_port = %s"
        params.append(origin)

    if destination:
        query += " AND ofl.arrival_port = %s"
        params.append(destination)

    query += " ORDER BY ofl.departure_time"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = rows[0].keys() if rows else []

    cursor.close()
    conn.close()

    return render_template(
        "booking_agent_page/booking_agent_flights.html",
        rows=rows,
        columns=columns,
        airports=airports,
        start_date=start_date,
        end_date=end_date,
        origin=origin,
        destination=destination
    )


# ----------------------------
# Route: Booking Agent Search
# Lets booking agents search available flights for their authorized airline.
# Also handles ticket purchases on behalf of customers.
# Enforces customer existence, airline authorization, status, and capacity.
# ----------------------------
@booking_agent_bp.route("/booking_agent_search", methods=["GET", "POST"])
def booking_agent_search():
    check = require_booking_agent()
    if check:
        return check

    agent_email = session.get("username")
    message = ""

    origin = request.form.get("origin", "").strip()
    destination = request.form.get("destination", "").strip()
    date = request.form.get("date", "").strip()
    action = request.form.get("action", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    agent_airline = get_agent_airline(cursor, agent_email)

    cursor.execute("""
        SELECT airport_name, city
        FROM airport
        ORDER BY city, airport_name
    """)
    airports = cursor.fetchall()

    if action == "buy":
        ticket_id = request.form.get("ticket_id", "").strip()
        customer_email = request.form.get("customer_email", "").strip()

        try:
            if not ticket_id or not customer_email:
                message = "Please select a ticket and enter a customer email."

            else:
                cursor.execute("""
                    SELECT customer_email
                    FROM customer
                    WHERE customer_email = %s
                """, (customer_email,))
                customer = cursor.fetchone()

                if not customer:
                    message = "Customer email does not exist."

                else:
                    cursor.execute("""
                        SELECT
                            t.ticket_id,
                            mf.marketing_airline_name,
                            ofl.status,
                            ac.seat_capacity - COALESCE(sold.sold_count, 0) AS seats_left
                        FROM ticket t
                        JOIN marketing_flight mf
                            ON t.marketing_airline_name = mf.marketing_airline_name
                           AND t.marketing_flight_num = mf.marketing_flight_num
                        JOIN operating_flight ofl
                            ON mf.operating_airline_name = ofl.operating_airline_name
                           AND mf.flight_number = ofl.flight_number
                        JOIN aircraft ac
                            ON ofl.aircraft_id = ac.aircraft_id
                        LEFT JOIN (
                            SELECT
                                mf2.operating_airline_name,
                                mf2.flight_number,
                                COUNT(cp.ticket_id) AS sold_count
                            FROM customer_purchases cp
                            JOIN ticket t2
                                ON cp.ticket_id = t2.ticket_id
                            JOIN marketing_flight mf2
                                ON t2.marketing_airline_name = mf2.marketing_airline_name
                               AND t2.marketing_flight_num = mf2.marketing_flight_num
                            GROUP BY
                                mf2.operating_airline_name,
                                mf2.flight_number
                        ) sold
                            ON sold.operating_airline_name = ofl.operating_airline_name
                           AND sold.flight_number = ofl.flight_number
                        WHERE t.ticket_id = %s
                    """, (ticket_id,))

                    ticket = cursor.fetchone()

                    if not ticket:
                        message = "Ticket does not exist."

                    elif ticket["marketing_airline_name"] != agent_airline:
                        message = "You are not authorized to sell this airline's tickets."

                    elif ticket["status"] not in ["upcoming", "delayed"]:
                        message = "Only upcoming or delayed flights can be purchased."

                    elif ticket["seats_left"] <= 0:
                        message = "This flight is sold out."

                    else:
                        cursor.execute("""
                            INSERT INTO customer_purchases(
                                customer_email,
                                ticket_id,
                                purchase_date
                            )
                            VALUES (%s, %s, NOW())
                        """, (customer_email, ticket_id))

                        cursor.execute("""
                            INSERT INTO booking_agent_purchases(
                                agent_email,
                                customer_email,
                                ticket_id,
                                purchase_date
                            )
                            VALUES (%s, %s, %s, NOW())
                        """, (agent_email, customer_email, ticket_id))

                        conn.commit()
                        message = "Purchase successful."

        except Exception as e:
            print("BOOKING AGENT BUY ERROR:", e)
            conn.rollback()
            message = "Purchase failed. This customer or agent may already have this ticket."

    query = """
        SELECT
            t.ticket_id,
            mf.marketing_airline_name,
            mf.marketing_flight_num,
            ofl.operating_airline_name,
            ofl.flight_number AS operating_flight_num,
            ofl.departure_port,
            ofl.arrival_port,
            ofl.departure_time,
            ofl.arrival_time,
            ofl.price,
            ROUND(ofl.price * %s, 2) AS commission,
            ofl.status,
            ac.seat_capacity - COALESCE(sold.sold_count, 0) AS seats_left
        FROM ticket t
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        JOIN aircraft ac
            ON ofl.aircraft_id = ac.aircraft_id
        LEFT JOIN (
            SELECT
                mf2.operating_airline_name,
                mf2.flight_number,
                COUNT(cp.ticket_id) AS sold_count
            FROM customer_purchases cp
            JOIN ticket t2
                ON cp.ticket_id = t2.ticket_id
            JOIN marketing_flight mf2
                ON t2.marketing_airline_name = mf2.marketing_airline_name
               AND t2.marketing_flight_num = mf2.marketing_flight_num
            GROUP BY
                mf2.operating_airline_name,
                mf2.flight_number
        ) sold
            ON sold.operating_airline_name = ofl.operating_airline_name
           AND sold.flight_number = ofl.flight_number
        WHERE mf.marketing_airline_name = %s
          AND ofl.status IN ('upcoming', 'delayed')
          AND ac.seat_capacity > COALESCE(sold.sold_count, 0)
    """

    params = [COMMISSION_RATE, agent_airline]

    if origin:
        query += " AND ofl.departure_port = %s"
        params.append(origin)

    if destination:
        query += " AND ofl.arrival_port = %s"
        params.append(destination)

    if date:
        query += " AND DATE(ofl.departure_time) = %s"
        params.append(date)

    query += " ORDER BY ofl.departure_time, t.ticket_id"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "booking_agent_page/booking_agent_search.html",
        rows=rows,
        airports=airports,
        message=message,
        origin=origin,
        destination=destination,
        date=date,
        agent_airline=agent_airline
    )


# ----------------------------
# Route: Booking Agent Analytics
# Shows commission totals, average commission, tickets sold,
# top customers by tickets, and top customers by commission.
# ----------------------------
@booking_agent_bp.route("/booking_agent_analytics", methods=["GET", "POST"])
def booking_agent_analytics():
    check = require_booking_agent()
    if check:
        return check

    agent_email = session.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COALESCE(SUM(ofl.price * %s), 0) AS total_commission,
            COALESCE(AVG(ofl.price * %s), 0) AS avg_commission,
            COUNT(*) AS tickets_sold
        FROM booking_agent_purchases bap
        JOIN ticket t
            ON bap.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE bap.agent_email = %s
          AND bap.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    """, (COMMISSION_RATE, COMMISSION_RATE, agent_email))
    summary = cursor.fetchone()

    cursor.execute("""
        SELECT
            bap.customer_email,
            COUNT(*) AS ticket_count
        FROM booking_agent_purchases bap
        WHERE bap.agent_email = %s
        AND bap.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY bap.customer_email
        ORDER BY ticket_count DESC
        LIMIT 5
    """, (agent_email,))
    top_customers_tickets = cursor.fetchall()

    cursor.execute("""
        SELECT
            bap.customer_email,
            ROUND(SUM(ofl.price * %s), 2) AS commission
        FROM booking_agent_purchases bap
        JOIN ticket t
            ON bap.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
        AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
        AND mf.flight_number = ofl.flight_number
        WHERE bap.agent_email = %s
        AND bap.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY bap.customer_email
        ORDER BY commission DESC
        LIMIT 5
    """, (COMMISSION_RATE, agent_email))
    top_customers_commission = cursor.fetchall()
    
    cursor.close()
    conn.close()

    max_ticket_count = max([row["ticket_count"] for row in top_customers_tickets], default=0)
    for row in top_customers_tickets:
        row["percent"] = 0 if max_ticket_count == 0 else round((row["ticket_count"] / max_ticket_count) * 100, 1)

    max_commission = max([float(row["commission"]) for row in top_customers_commission], default=0)
    for row in top_customers_commission:
        amount = float(row["commission"])
        row["percent"] = 0 if max_commission == 0 else round((amount / max_commission) * 100, 1)

    return render_template(
        "booking_agent_page/booking_agent_analytics.html",
        summary=summary,
        top_customers_tickets=top_customers_tickets,
        top_customers_commission=top_customers_commission
    )