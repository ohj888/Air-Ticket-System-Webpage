from flask import Blueprint, render_template, session, redirect, url_for, abort, request
from db import get_db_connection
from datetime import date

customer_bp = Blueprint("customer", __name__)

# protection method
def require_customer():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("user_type") != "customer":
        abort(403)


@customer_bp.route("/customer_home")
def customer_home():
    check = require_customer()
    if check:
        return check

    return render_template(
        "customer_page/customer_home.html",
        username=session.get("username")
    )


# find my flights --------
@customer_bp.route("/customer_flights", methods=["GET", "POST"])
def customer_flights():
    check = require_customer()
    if check:
        return check

    username = session.get("username")

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
            cp.purchase_date,
            cp.ticket_id,
            mf.marketing_airline_name,
            mf.marketing_flight_num,
            ofl.operating_airline_name,
            ofl.flight_number AS operating_flight_num,
            ofl.departure_port,
            ofl.arrival_port,
            ofl.departure_time,
            ofl.arrival_time,
            ofl.price,
            ofl.status
        FROM customer_purchases cp
        JOIN ticket t
            ON cp.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE cp.customer_email = %s
    """

    params = [username]

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

    query += """
        ORDER BY ofl.departure_time
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = rows[0].keys() if rows else []

    cursor.close()
    conn.close()

    return render_template(
        "customer_page/customer_flights.html",
        rows=rows,
        columns=columns,
        airports=airports,
        start_date=start_date,
        end_date=end_date,
        origin=origin,
        destination=destination
    )
# --------

# Search new flights --------
@customer_bp.route("/customer_search", methods=["GET", "POST"])
def customer_search():
    check = require_customer()
    if check:
        return check

    username = session.get("username")
    message = ""

    origin = request.form.get("origin", "").strip()
    destination = request.form.get("destination", "").strip()
    date = request.form.get("date", "").strip()
    action = request.form.get("action", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # buy ticket
    if action == "buy":
        ticket_id = request.form.get("ticket_id", "").strip()

        try:
            if not ticket_id:
                message = "No ticket selected."

            else:
                cursor.execute("""
                    SELECT
                        t.ticket_id,
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
                    """, (username, ticket_id))

                    conn.commit()
                    message = "Purchase successful."

        except Exception as e:
            print("BUY ERROR:", e)
            conn.rollback()
            message = "Purchase failed."

    # airport dropdowns
    cursor.execute("""
        SELECT airport_name, city
        FROM airport
        ORDER BY city, airport_name
    """)
    airports = cursor.fetchall()

    # ticket table with filters
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
        WHERE ofl.status IN ('upcoming', 'delayed')
        AND ac.seat_capacity > COALESCE(sold.sold_count, 0)
    """

    params = []

    if origin:
        query += " AND ofl.departure_port = %s"
        params.append(origin)

    if destination:
        query += " AND ofl.arrival_port = %s"
        params.append(destination)

    if date:
        query += " AND DATE(ofl.departure_time) = %s"
        params.append(date)

    query += """
        ORDER BY ofl.departure_time, t.ticket_id
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "customer_page/customer_search.html",
        rows=rows,
        airports=airports,
        message=message,
        origin=origin,
        destination=destination,
        date=date
    )

# spending --------
@customer_bp.route("/customer_spending", methods=["GET", "POST"])
def customer_spending():
    check = require_customer()
    if check:
        return check

    username = session.get("username")
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST" and start_date and end_date:
        # custom view
        cursor.execute("""
            SELECT COALESCE(SUM(ofl.price), 0) AS total_spending
            FROM customer_purchases cp
            JOIN ticket t
                ON cp.ticket_id = t.ticket_id
            JOIN marketing_flight mf
                ON t.marketing_airline_name = mf.marketing_airline_name
               AND t.marketing_flight_num = mf.marketing_flight_num
            JOIN operating_flight ofl
                ON mf.operating_airline_name = ofl.operating_airline_name
               AND mf.flight_number = ofl.flight_number
            WHERE cp.customer_email = %s
              AND DATE(cp.purchase_date) BETWEEN %s AND %s
        """, (username, start_date, end_date))

        total_spending = cursor.fetchone()["total_spending"]

        cursor.execute("""
            SELECT
                DATE_FORMAT(cp.purchase_date, '%Y-%m') AS month,
                COALESCE(SUM(ofl.price), 0) AS amount
            FROM customer_purchases cp
            JOIN ticket t
                ON cp.ticket_id = t.ticket_id
            JOIN marketing_flight mf
                ON t.marketing_airline_name = mf.marketing_airline_name
               AND t.marketing_flight_num = mf.marketing_flight_num
            JOIN operating_flight ofl
                ON mf.operating_airline_name = ofl.operating_airline_name
               AND mf.flight_number = ofl.flight_number
            WHERE cp.customer_email = %s
              AND DATE(cp.purchase_date) BETWEEN %s AND %s
            GROUP BY DATE_FORMAT(cp.purchase_date, '%Y-%m')
            ORDER BY month
        """, (username, start_date, end_date))

        monthly_spending = cursor.fetchall()
        view_title = "Custom Spending View"

    else:
        # default view
        cursor.execute("""
            SELECT COALESCE(SUM(ofl.price), 0) AS total_spending
            FROM customer_purchases cp
            JOIN ticket t
                ON cp.ticket_id = t.ticket_id
            JOIN marketing_flight mf
                ON t.marketing_airline_name = mf.marketing_airline_name
               AND t.marketing_flight_num = mf.marketing_flight_num
            JOIN operating_flight ofl
                ON mf.operating_airline_name = ofl.operating_airline_name
               AND mf.flight_number = ofl.flight_number
            WHERE cp.customer_email = %s
              AND cp.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        """, (username,))

        total_spending = cursor.fetchone()["total_spending"]

        cursor.execute("""
            SELECT
                DATE_FORMAT(cp.purchase_date, '%Y-%m') AS month,
                COALESCE(SUM(ofl.price), 0) AS amount
            FROM customer_purchases cp
            JOIN ticket t
                ON cp.ticket_id = t.ticket_id
            JOIN marketing_flight mf
                ON t.marketing_airline_name = mf.marketing_airline_name
               AND t.marketing_flight_num = mf.marketing_flight_num
            JOIN operating_flight ofl
                ON mf.operating_airline_name = ofl.operating_airline_name
               AND mf.flight_number = ofl.flight_number
            WHERE cp.customer_email = %s
              AND cp.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(cp.purchase_date, '%Y-%m')
            ORDER BY month
        """, (username,))

        monthly_spending = cursor.fetchall()
        view_title = "Default Spending View"
        
        # force last 6 months to show left-to-right, ending with current month
        today = date.today()
        month_labels = []

        year = today.year
        month = today.month

        for i in range(5, -1, -1):
            m = month - i
            y = year

            while m <= 0:
                m += 12
                y -= 1

            month_labels.append(f"{y}-{m:02d}")

        spending_map = {
            row["month"]: row["amount"]
            for row in monthly_spending
        }

        monthly_spending = [
            {
                "month": month_label,
                "amount": spending_map.get(month_label, 0)
            }
            for month_label in month_labels
        ]

        cursor.close()
        conn.close()

    max_amount = max([float(row["amount"]) for row in monthly_spending], default=0)

    for row in monthly_spending:
        amount = float(row["amount"])
        row["percent"] = 0 if max_amount == 0 else round((amount / max_amount) * 100, 1)

    return render_template(
        "customer_page/customer_spending.html",
        total_spending=total_spending,
        monthly_spending=monthly_spending,
        start_date=start_date,
        end_date=end_date,
        view_title=view_title
    )
# --------