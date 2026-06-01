from flask import Blueprint, render_template, session, redirect, url_for, abort, request
from db import get_db_connection
from datetime import datetime

airline_staff_bp = Blueprint("airline_staff", __name__)

COMMISSION_RATE = 0.10

ALLOWED_AIRPORTS = [
    {"airport_name": "ATL", "airport_full_name": "Hartsfield-Jackson Atlanta International Airport", "city": "Atlanta", "state": "GA"},
    {"airport_name": "ORD", "airport_full_name": "O'Hare International Airport", "city": "Chicago", "state": "IL"},
    {"airport_name": "DFW", "airport_full_name": "Dallas/Fort Worth International Airport", "city": "Dallas", "state": "TX"},
    {"airport_name": "DEN", "airport_full_name": "Denver International Airport", "city": "Denver", "state": "CO"},
    {"airport_name": "SEA", "airport_full_name": "Seattle-Tacoma International Airport", "city": "Seattle", "state": "WA"},
    {"airport_name": "BOS", "airport_full_name": "Boston Logan International Airport", "city": "Boston", "state": "MA"},

    {"airport_name": "PEK", "airport_full_name": "Beijing Capital International Airport", "city": "Beijing", "state": "Beijing"},
    {"airport_name": "PKX", "airport_full_name": "Beijing Daxing International Airport", "city": "Beijing", "state": "Beijing"},
    {"airport_name": "CAN", "airport_full_name": "Guangzhou Baiyun International Airport", "city": "Guangzhou", "state": "GD"},
    {"airport_name": "CTU", "airport_full_name": "Chengdu Shuangliu International Airport", "city": "Chengdu", "state": "SC"},
    {"airport_name": "TFU", "airport_full_name": "Chengdu Tianfu International Airport", "city": "Chengdu", "state": "SC"},
    {"airport_name": "HKG", "airport_full_name": "Hong Kong International Airport", "city": "Hong Kong", "state": "Hong Kong"},

    {"airport_name": "KIX", "airport_full_name": "Kansai International Airport", "city": "Osaka", "state": "Osaka"},
    {"airport_name": "FUK", "airport_full_name": "Fukuoka Airport", "city": "Fukuoka", "state": "Fukuoka"},
    {"airport_name": "CTS", "airport_full_name": "New Chitose Airport", "city": "Sapporo", "state": "Hokkaido"},

    {"airport_name": "BKK", "airport_full_name": "Suvarnabhumi Airport", "city": "Bangkok", "state": "Bangkok"},
    {"airport_name": "DMK", "airport_full_name": "Don Mueang International Airport", "city": "Bangkok", "state": "Bangkok"},
    {"airport_name": "KUL", "airport_full_name": "Kuala Lumpur International Airport", "city": "Kuala Lumpur", "state": "Selangor"},
    {"airport_name": "CGK", "airport_full_name": "Soekarno-Hatta International Airport", "city": "Jakarta", "state": "Banten"},
    {"airport_name": "MNL", "airport_full_name": "Ninoy Aquino International Airport", "city": "Manila", "state": "Metro Manila"},
    {"airport_name": "SGN", "airport_full_name": "Tan Son Nhat International Airport", "city": "Ho Chi Minh City", "state": "Ho Chi Minh City"},
    {"airport_name": "HAN", "airport_full_name": "Noi Bai International Airport", "city": "Hanoi", "state": "Hanoi"},

    {"airport_name": "DEL", "airport_full_name": "Indira Gandhi International Airport", "city": "Delhi", "state": "Delhi"},
    {"airport_name": "BOM", "airport_full_name": "Chhatrapati Shivaji Maharaj International Airport", "city": "Mumbai", "state": "Maharashtra"},
    {"airport_name": "BLR", "airport_full_name": "Kempegowda International Airport", "city": "Bengaluru", "state": "Karnataka"},

    {"airport_name": "DXB", "airport_full_name": "Dubai International Airport", "city": "Dubai", "state": "Dubai"},
    {"airport_name": "AUH", "airport_full_name": "Zayed International Airport", "city": "Abu Dhabi", "state": "Abu Dhabi"},
    {"airport_name": "IST", "airport_full_name": "Istanbul Airport", "city": "Istanbul", "state": "Istanbul"},

    {"airport_name": "FRA", "airport_full_name": "Frankfurt Airport", "city": "Frankfurt", "state": "Hesse"},
    {"airport_name": "MUC", "airport_full_name": "Munich Airport", "city": "Munich", "state": "Bavaria"},
    {"airport_name": "AMS", "airport_full_name": "Amsterdam Airport Schiphol", "city": "Amsterdam", "state": "North Holland"},
    {"airport_name": "MAD", "airport_full_name": "Adolfo Suárez Madrid-Barajas Airport", "city": "Madrid", "state": "Madrid"},
    {"airport_name": "BCN", "airport_full_name": "Barcelona-El Prat Airport", "city": "Barcelona", "state": "Catalonia"},
    {"airport_name": "FCO", "airport_full_name": "Leonardo da Vinci-Fiumicino Airport", "city": "Rome", "state": "Lazio"},
    {"airport_name": "ZRH", "airport_full_name": "Zurich Airport", "city": "Zurich", "state": "Zurich"},

    {"airport_name": "SYD", "airport_full_name": "Sydney Kingsford Smith Airport", "city": "Sydney", "state": "NSW"},
    {"airport_name": "MEL", "airport_full_name": "Melbourne Airport", "city": "Melbourne", "state": "VIC"},
    {"airport_name": "AKL", "airport_full_name": "Auckland Airport", "city": "Auckland", "state": "Auckland"},

    {"airport_name": "YYZ", "airport_full_name": "Toronto Pearson International Airport", "city": "Toronto", "state": "Ontario"},
    {"airport_name": "YVR", "airport_full_name": "Vancouver International Airport", "city": "Vancouver", "state": "British Columbia"},
    {"airport_name": "MEX", "airport_full_name": "Mexico City International Airport", "city": "Mexico City", "state": "CDMX"},

    {"airport_name": "GRU", "airport_full_name": "São Paulo/Guarulhos International Airport", "city": "São Paulo", "state": "São Paulo"},
    {"airport_name": "EZE", "airport_full_name": "Ministro Pistarini International Airport", "city": "Buenos Aires", "state": "Buenos Aires"},
    {"airport_name": "SCL", "airport_full_name": "Arturo Merino Benítez International Airport", "city": "Santiago", "state": "Santiago"},

    {"airport_name": "JNB", "airport_full_name": "O. R. Tambo International Airport", "city": "Johannesburg", "state": "Gauteng"},
    {"airport_name": "CPT", "airport_full_name": "Cape Town International Airport", "city": "Cape Town", "state": "Western Cape"},
    {"airport_name": "CAI", "airport_full_name": "Cairo International Airport", "city": "Cairo", "state": "Cairo"}
]

ALLOWED_AIRCRAFT_TYPES = [
    {"code": "A320", "seat_capacity": 180},
    {"code": "A330", "seat_capacity": 280},
    {"code": "A350", "seat_capacity": 300},
    {"code": "B737", "seat_capacity": 160},
    {"code": "B777", "seat_capacity": 310},
    {"code": "B787", "seat_capacity": 260}
]

AIRLINE_CODE_PREFIXES = {
    "Air China": "CA",
    "China Eastern": "MU",
    "Delta Air Lines": "DL",
    "United Airlines": "UA",
    "Japan Airlines": "JL",
    "Korean Air": "KE",
    "Singapore Airlines": "SQ",
    "Air France": "AF",
    "British Airways": "BA",
    "Qatar Airways": "QR",
    "Shenzhen Airlines": "ZH"
}

ALLOWED_CODESHARE_NUMBERS = [
    "8501",
    "8502",
    "8503",
    "8504",
    "8505",
    "8601",
    "8602",
    "8603",
    "8701",
    "8702"
]

# helper
def is_positive_integer(value):
    return value.isdigit() and int(value) > 0


def is_positive_price(value):
    try:
        return float(value) > 0
    except ValueError:
        return False
# --------

# ----------------------------
# Helper: only airline staff can access these pages
# ----------------------------
def require_airline_staff():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if session.get("user_type") != "airline_staff":
        abort(403)


# ----------------------------
# Helper: get staff airline and permissions
# ----------------------------
def get_staff_info(cursor, username):
    cursor.execute("""
        SELECT airline_name
        FROM airline_staff
        WHERE staff_username = %s
    """, (username,))
    staff = cursor.fetchone()

    if not staff:
        return None, []

    cursor.execute("""
        SELECT permission
        FROM staff_permissions
        WHERE staff_username = %s
    """, (username,))
    permissions = [row["permission"] for row in cursor.fetchall()]

    return staff["airline_name"], permissions


# ----------------------------
# Route: Airline Staff Home
# Shows flights operated by staff airline.
# Default: next 30 days.
# Filters: date range, origin, destination.
# ----------------------------
@airline_staff_bp.route("/airline_staff_home", methods=["GET", "POST"])
def airline_staff_home():
    check = require_airline_staff()
    if check:
        return check

    username = session.get("username")

    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    origin = request.form.get("origin", "").strip()
    destination = request.form.get("destination", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    airline_name, permissions = get_staff_info(cursor, username)

    cursor.execute("""
        SELECT airport_name, city
        FROM airport
        ORDER BY city, airport_name
    """)
    airports = cursor.fetchall()

    query = """
        SELECT
            flight_number,
            departure_port,
            arrival_port,
            departure_time,
            arrival_time,
            price,
            status,
            aircraft_id
        FROM operating_flight
        WHERE operating_airline_name = %s
    """

    params = [airline_name]

    if start_date or end_date:
        if start_date:
            query += " AND DATE(departure_time) >= %s"
            params.append(start_date)

        if end_date:
            query += " AND DATE(departure_time) <= %s"
            params.append(end_date)
    else:
        query += """
            AND departure_time >= NOW()
            AND departure_time < DATE_ADD(NOW(), INTERVAL 30 DAY)
        """

    if origin:
        query += " AND departure_port = %s"
        params.append(origin)

    if destination:
        query += " AND arrival_port = %s"
        params.append(destination)

    query += " ORDER BY departure_time"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = rows[0].keys() if rows else []

    cursor.close()
    conn.close()

    return render_template(
        "airline_staff_page/airline_staff_home.html",
        username=username,
        airline_name=airline_name,
        permissions=permissions,
        rows=rows,
        columns=columns,
        airports=airports,
        start_date=start_date,
        end_date=end_date,
        origin=origin,
        destination=destination
    )


# ----------------------------
# Route: Passenger List
# Staff selects a flight operated by their airline.
# Shows customers who purchased tickets for that flight.
# ----------------------------
@airline_staff_bp.route("/airline_staff_passengers", methods=["GET", "POST"])
def airline_staff_passengers():
    check = require_airline_staff()
    if check:
        return check

    username = session.get("username")
    selected_flight = request.form.get("flight_number", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    airline_name, permissions = get_staff_info(cursor, username)

    cursor.execute("""
        SELECT flight_number, departure_port, arrival_port, departure_time
        FROM operating_flight
        WHERE operating_airline_name = %s
        ORDER BY departure_time
    """, (airline_name,))
    flights = cursor.fetchall()

    passengers = []

    if selected_flight:
        cursor.execute("""
            SELECT
                cp.customer_email,
                c.name,
                c.phone_number,
                t.ticket_id,
                mf.marketing_airline_name,
                mf.marketing_flight_num,
                cp.purchase_date
            FROM customer_purchases cp
            JOIN customer c
                ON cp.customer_email = c.customer_email
            JOIN ticket t
                ON cp.ticket_id = t.ticket_id
            JOIN marketing_flight mf
                ON t.marketing_airline_name = mf.marketing_airline_name
               AND t.marketing_flight_num = mf.marketing_flight_num
            JOIN operating_flight ofl
                ON mf.operating_airline_name = ofl.operating_airline_name
               AND mf.flight_number = ofl.flight_number
            WHERE ofl.operating_airline_name = %s
              AND ofl.flight_number = %s
            ORDER BY c.name
        """, (airline_name, selected_flight))
        passengers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "airline_staff_page/airline_staff_passengers.html",
        airline_name=airline_name,
        flights=flights,
        passengers=passengers,
        selected_flight=selected_flight
    )


# ----------------------------
# Route: Customer Flight History
# Staff enters customer email.
# Shows all flights that customer took on staff airline.
# ----------------------------
@airline_staff_bp.route("/airline_staff_customer_history", methods=["GET", "POST"])
def airline_staff_customer_history():
    check = require_airline_staff()
    if check:
        return check

    username = session.get("username")
    customer_email = request.form.get("customer_email", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    airline_name, permissions = get_staff_info(cursor, username)

    rows = []

    if customer_email:
        cursor.execute("""
            SELECT
                cp.customer_email,
                cp.ticket_id,
                mf.marketing_airline_name,
                mf.marketing_flight_num,
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
              AND ofl.operating_airline_name = %s
            ORDER BY ofl.departure_time
        """, (customer_email, airline_name))
        rows = cursor.fetchall()

    columns = rows[0].keys() if rows else []

    cursor.close()
    conn.close()

    return render_template(
        "airline_staff_page/airline_staff_customer_history.html",
        airline_name=airline_name,
        customer_email=customer_email,
        rows=rows,
        columns=columns
    )


# ----------------------------
# Route: Airline Staff Analytics
# Includes:
# - top booking agents this month/year by tickets
# - top booking agents this month/year by commission
# - most frequent customer last year
# - tickets sold per month
# - delay vs on-time stats
# - top destinations last 3 months and last year
# ----------------------------
@airline_staff_bp.route("/airline_staff_analytics")
def airline_staff_analytics():
    check = require_airline_staff()
    if check:
        return check

    username = session.get("username")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    airline_name, permissions = get_staff_info(cursor, username)

    def add_percent(rows, value_key):
        max_value = max([float(row[value_key]) for row in rows], default=0)
        for row in rows:
            value = float(row[value_key])
            row["percent"] = 0 if max_value == 0 else round((value / max_value) * 100, 1)

    # Top agents this month by tickets
    cursor.execute("""
        SELECT
            bap.agent_email,
            COUNT(*) AS tickets_sold
        FROM booking_agent_purchases bap
        JOIN ticket t ON bap.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND MONTH(bap.purchase_date) = MONTH(CURDATE())
          AND YEAR(bap.purchase_date) = YEAR(CURDATE())
        GROUP BY bap.agent_email
        ORDER BY tickets_sold DESC
        LIMIT 5
    """, (airline_name,))
    top_agents_month_tickets = cursor.fetchall()
    add_percent(top_agents_month_tickets, "tickets_sold")

    # Top agents this year by tickets
    cursor.execute("""
        SELECT
            bap.agent_email,
            COUNT(*) AS tickets_sold
        FROM booking_agent_purchases bap
        JOIN ticket t ON bap.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND YEAR(bap.purchase_date) = YEAR(CURDATE())
        GROUP BY bap.agent_email
        ORDER BY tickets_sold DESC
        LIMIT 5
    """, (airline_name,))
    top_agents_year_tickets = cursor.fetchall()
    add_percent(top_agents_year_tickets, "tickets_sold")

    # Top agents this month by commission
    cursor.execute("""
        SELECT
            bap.agent_email,
            ROUND(SUM(ofl.price * %s), 2) AS commission
        FROM booking_agent_purchases bap
        JOIN ticket t ON bap.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND MONTH(bap.purchase_date) = MONTH(CURDATE())
          AND YEAR(bap.purchase_date) = YEAR(CURDATE())
        GROUP BY bap.agent_email
        ORDER BY commission DESC
        LIMIT 5
    """, (COMMISSION_RATE, airline_name))
    top_agents_month_commission = cursor.fetchall()
    add_percent(top_agents_month_commission, "commission")

    # Top agents this year by commission
    cursor.execute("""
        SELECT
            bap.agent_email,
            ROUND(SUM(ofl.price * %s), 2) AS commission
        FROM booking_agent_purchases bap
        JOIN ticket t ON bap.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND YEAR(bap.purchase_date) = YEAR(CURDATE())
        GROUP BY bap.agent_email
        ORDER BY commission DESC
        LIMIT 5
    """, (COMMISSION_RATE, airline_name))
    top_agents_year_commission = cursor.fetchall()
    add_percent(top_agents_year_commission, "commission")

    # Most frequent customer last year
    cursor.execute("""
        SELECT
            cp.customer_email,
            COUNT(*) AS tickets_bought
        FROM customer_purchases cp
        JOIN ticket t ON cp.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND cp.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY cp.customer_email
        ORDER BY tickets_bought DESC
        LIMIT 1
    """, (airline_name,))
    frequent_customer = cursor.fetchone()

    # Tickets sold per month, last 12 months
    cursor.execute("""
        SELECT
            DATE_FORMAT(cp.purchase_date, '%Y-%m') AS month,
            COUNT(*) AS tickets_sold
        FROM customer_purchases cp
        JOIN ticket t ON cp.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND cp.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY DATE_FORMAT(cp.purchase_date, '%Y-%m')
        ORDER BY month
    """, (airline_name,))
    tickets_per_month = cursor.fetchall()
    add_percent(tickets_per_month, "tickets_sold")

    # Delay vs on-time stats
    cursor.execute("""
        SELECT
            SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) AS delayed_count,
            SUM(CASE WHEN status <> 'delayed' THEN 1 ELSE 0 END) AS on_time_count,
            COUNT(*) AS total_flights
        FROM operating_flight
        WHERE operating_airline_name = %s
    """, (airline_name,))
    delay_stats = cursor.fetchone()

    # Top destinations last 3 months
    cursor.execute("""
        SELECT
            ofl.arrival_port,
            COUNT(*) AS tickets_sold
        FROM customer_purchases cp
        JOIN ticket t ON cp.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND cp.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
        GROUP BY ofl.arrival_port
        ORDER BY tickets_sold DESC
        LIMIT 5
    """, (airline_name,))
    top_destinations_3_months = cursor.fetchall()
    add_percent(top_destinations_3_months, "tickets_sold")

    # Top destinations last year
    cursor.execute("""
        SELECT
            ofl.arrival_port,
            COUNT(*) AS tickets_sold
        FROM customer_purchases cp
        JOIN ticket t ON cp.ticket_id = t.ticket_id
        JOIN marketing_flight mf
            ON t.marketing_airline_name = mf.marketing_airline_name
           AND t.marketing_flight_num = mf.marketing_flight_num
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE ofl.operating_airline_name = %s
          AND cp.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY ofl.arrival_port
        ORDER BY tickets_sold DESC
        LIMIT 5
    """, (airline_name,))
    top_destinations_year = cursor.fetchall()
    add_percent(top_destinations_year, "tickets_sold")

    cursor.close()
    conn.close()

    return render_template(
        "airline_staff_page/airline_staff_analytics.html",
        airline_name=airline_name,
        top_agents_month_tickets=top_agents_month_tickets,
        top_agents_year_tickets=top_agents_year_tickets,
        top_agents_month_commission=top_agents_month_commission,
        top_agents_year_commission=top_agents_year_commission,
        frequent_customer=frequent_customer,
        tickets_per_month=tickets_per_month,
        delay_stats=delay_stats,
        top_destinations_3_months=top_destinations_3_months,
        top_destinations_year=top_destinations_year
    )


# ----------------------------
# Route: Admin Tools
# Admin can:
# - add airports
# - add aircraft
# - create flights
# - associate booking agents
# ----------------------------
@airline_staff_bp.route("/airline_staff_admin", methods=["GET", "POST"])
def airline_staff_admin():
    check = require_airline_staff()
    if check:
        return check

    username = session.get("username")
    message = ""

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    airline_name, permissions = get_staff_info(cursor, username)

    if "Admin" not in permissions:
        cursor.close()
        conn.close()
        abort(403)

    airline_prefix = AIRLINE_CODE_PREFIXES.get(airline_name, airline_name[:2].upper())
    action = request.form.get("action", "").strip()

    try:
        if request.method == "POST":

            if action == "add_airport":
                selected_airport = request.form.get("airport_name", "").strip()

                airport_data = None
                for airport in ALLOWED_AIRPORTS:
                    if airport["airport_name"] == selected_airport:
                        airport_data = airport
                        break

                if not airport_data:
                    message = "Please select an airport."
                else:
                    cursor.execute("""
                        SELECT airport_name
                        FROM airport
                        WHERE airport_name = %s
                    """, (airport_data["airport_name"],))

                    existing_airport = cursor.fetchone()

                    if existing_airport:
                        message = "Airport already exists."
                    else:
                        cursor.execute("""
                            INSERT INTO airport(
                                airport_name,
                                city
                            )
                            VALUES (%s, %s)
                        """, (
                            airport_data["airport_name"],
                            airport_data["city"]
                        ))

                        conn.commit()
                        message = "Airport added successfully."
            elif action == "add_aircraft":
                aircraft_type = request.form.get("aircraft_type", "").strip()
                aircraft_number = request.form.get("aircraft_number", "").strip()

                aircraft_data = None
                for plane in ALLOWED_AIRCRAFT_TYPES:
                    if plane["code"] == aircraft_type:
                        aircraft_data = plane
                        break

                if not aircraft_data:
                    message = "Please select a valid aircraft type."

                elif not is_positive_integer(aircraft_number):
                    message = "Aircraft number must be a positive number."

                else:
                    aircraft_id = f"{airline_prefix}-{aircraft_type}-{aircraft_number.zfill(3)}"

                    cursor.execute("""
                        SELECT aircraft_id
                        FROM aircraft
                        WHERE aircraft_id = %s
                    """, (aircraft_id,))

                    existing_aircraft = cursor.fetchone()

                    if existing_aircraft:
                        message = f"Aircraft {aircraft_id} already exists."

                    else:
                        cursor.execute("""
                            INSERT INTO aircraft(
                                aircraft_id,
                                seat_capacity,
                                airline_name
                            )
                            VALUES (%s, %s, %s)
                        """, (
                            aircraft_id,
                            aircraft_data["seat_capacity"],
                            airline_name
                        ))

                        conn.commit()
                        message = f"Aircraft {aircraft_id} added successfully."

            elif action == "create_flight":
                flight_number_suffix = request.form.get("flight_number_suffix", "").strip()
                departure_time = request.form.get("departure_time", "").strip()
                arrival_time = request.form.get("arrival_time", "").strip()
                price = request.form.get("price", "").strip()
                status = request.form.get("status", "").strip()
                departure_port = request.form.get("departure_port", "").strip()
                arrival_port = request.form.get("arrival_port", "").strip()
                aircraft_id = request.form.get("aircraft_id", "").strip()

                allowed_statuses = ["upcoming", "delayed", "in-progress", "completed"]

                if not is_positive_integer(flight_number_suffix):
                    message = "Flight number must be a positive number."

                elif not is_positive_price(price):
                    message = "Price must be positive."

                elif status not in allowed_statuses:
                    message = "Invalid flight status."

                elif departure_port == arrival_port:
                    message = "Departure and arrival airports cannot be the same."

                else:
                    flight_number = f"{airline_prefix}{flight_number_suffix}"

                    departure_dt = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M")
                    arrival_dt = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M")

                    if arrival_dt <= departure_dt:
                        message = "Arrival time must be after departure time."

                    else:
                        # Check flight does not already exist
                        cursor.execute("""
                            SELECT flight_number
                            FROM operating_flight
                            WHERE operating_airline_name = %s
                            AND flight_number = %s
                        """, (airline_name, flight_number))

                        existing_flight = cursor.fetchone()

                        # Check aircraft belongs to this airline
                        cursor.execute("""
                            SELECT aircraft_id
                            FROM aircraft
                            WHERE aircraft_id = %s
                            AND airline_name = %s
                        """, (aircraft_id, airline_name))

                        valid_aircraft = cursor.fetchone()

                        if existing_flight:
                            message = f"Flight {flight_number} already exists."

                        elif not valid_aircraft:
                            message = "Selected aircraft does not belong to your airline."

                        else:
                            cursor.execute("""
                                INSERT INTO operating_flight(
                                    operating_airline_name,
                                    flight_number,
                                    departure_time,
                                    arrival_time,
                                    price,
                                    status,
                                    departure_port,
                                    arrival_port,
                                    aircraft_id
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                airline_name,
                                flight_number,
                                departure_time,
                                arrival_time,
                                price,
                                status,
                                departure_port,
                                arrival_port,
                                aircraft_id
                            ))

                            cursor.execute("""
                                INSERT INTO marketing_flight(
                                    marketing_airline_name,
                                    marketing_flight_num,
                                    operating_airline_name,
                                    flight_number
                                )
                                VALUES (%s, %s, %s, %s)
                            """, (
                                airline_name,
                                flight_number,
                                airline_name,
                                flight_number
                            ))

                            cursor.execute("""
                                SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_id, 6) AS UNSIGNED)), 0) + 1 AS next_ticket_num
                                FROM ticket
                                WHERE ticket_id LIKE 'TCKT-%'
                            """)
                            next_ticket_num = cursor.fetchone()["next_ticket_num"]
                            new_ticket_id = "TCKT-" + str(next_ticket_num).zfill(3)

                            cursor.execute("""
                                INSERT INTO ticket(
                                    ticket_id,
                                    marketing_airline_name,
                                    marketing_flight_num
                                )
                                VALUES (%s, %s, %s)
                            """, (
                                new_ticket_id,
                                airline_name,
                                flight_number
                            ))

                            conn.commit()
                            message = f"Flight {flight_number} created successfully with ticket {new_ticket_id}."

            elif action == "add_codeshare":
                partner_airline_name = request.form.get("partner_airline_name", "").strip()
                codeshare_number = request.form.get("codeshare_number", "").strip()
                operating_flight_number = request.form.get("operating_flight_number", "").strip()

                if not partner_airline_name or not codeshare_number or not operating_flight_number:
                    message = "Please fill in all code-share fields."

                elif codeshare_number not in ALLOWED_CODESHARE_NUMBERS:
                    message = "Invalid code-share number selected."

                else:
                    partner_prefix = AIRLINE_CODE_PREFIXES.get(
                        partner_airline_name,
                        partner_airline_name[:2].upper()
                    )

                    marketing_flight_num = f"{partner_prefix}{codeshare_number}"

                    # 1. Check partner airline exists
                    cursor.execute("""
                        SELECT airline_name
                        FROM airline
                        WHERE airline_name = %s
                    """, (partner_airline_name,))
                    partner_airline = cursor.fetchone()

                    # 2. Check the selected operating flight belongs to the staff airline
                    cursor.execute("""
                        SELECT flight_number
                        FROM operating_flight
                        WHERE operating_airline_name = %s
                        AND flight_number = %s
                    """, (airline_name, operating_flight_number))
                    operating_flight = cursor.fetchone()

                    # 3. Check this exact marketing flight does not already exist
                    cursor.execute("""
                        SELECT marketing_airline_name, marketing_flight_num
                        FROM marketing_flight
                        WHERE marketing_airline_name = %s
                        AND marketing_flight_num = %s
                    """, (partner_airline_name, marketing_flight_num))
                    existing_codeshare = cursor.fetchone()

                    if not partner_airline:
                        message = "Partner airline does not exist."

                    elif not operating_flight:
                        message = "Selected operating flight does not belong to your airline."

                    elif existing_codeshare:
                        message = f"Marketing flight {marketing_flight_num} already exists for {partner_airline_name}."

                    else:
                        cursor.execute("""
                            INSERT INTO marketing_flight(
                                marketing_airline_name,
                                marketing_flight_num,
                                operating_airline_name,
                                flight_number
                            )
                            VALUES (%s, %s, %s, %s)
                        """, (
                            partner_airline_name,
                            marketing_flight_num,
                            airline_name,
                            operating_flight_number
                        ))

                        conn.commit()
                        message = f"Code-share flight {marketing_flight_num} added successfully."

    except Exception as e:
        print("ADMIN ERROR:", e)
        conn.rollback()
        message = "Action failed. Check duplicate keys or invalid foreign keys."

    cursor.execute("""
        SELECT airport_name, city
        FROM airport
        ORDER BY city, airport_name
    """)
    airports = cursor.fetchall()

    cursor.execute("""
        SELECT aircraft_id
        FROM aircraft
        WHERE airline_name = %s
        ORDER BY aircraft_id
    """, (airline_name,))
    aircraft = cursor.fetchall()

    cursor.execute("""
        SELECT agent_email, airline_name
        FROM booking_agent
        ORDER BY agent_email
    """)
    booking_agents = cursor.fetchall()

    cursor.execute("""
        SELECT airline_name
        FROM airline
        WHERE airline_name <> %s
        ORDER BY airline_name
    """, (airline_name,))
    partner_airlines = cursor.fetchall()

    cursor.execute("""
        SELECT flight_number, departure_port, arrival_port, departure_time
        FROM operating_flight
        WHERE operating_airline_name = %s
        ORDER BY departure_time
    """, (airline_name,))
    operating_flights = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "airline_staff_page/airline_staff_admin.html",
        airline_name=airline_name,
        airline_prefix=airline_prefix,
        message=message,
        airports=airports,
        aircraft=aircraft,
        booking_agents=booking_agents,
        allowed_airports=ALLOWED_AIRPORTS,
        allowed_aircraft_types=ALLOWED_AIRCRAFT_TYPES,
        partner_airlines=partner_airlines,
        operating_flights=operating_flights, 
        allowed_codeshare_numbers=ALLOWED_CODESHARE_NUMBERS
    )


# ----------------------------
# Route: Operator Tools
# Operator can update flight statuses
# ----------------------------
@airline_staff_bp.route("/airline_staff_operator", methods=["GET", "POST"])
def airline_staff_operator():
    check = require_airline_staff()
    if check:
        return check

    username = session.get("username")
    message = ""

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    airline_name, permissions = get_staff_info(cursor, username)

    if "Operator" not in permissions:
        cursor.close()
        conn.close()
        abort(403)

    if request.method == "POST":
        flight_number = request.form.get("flight_number", "").strip()
        status = request.form.get("status", "").strip()

        try:
            cursor.execute("""
                UPDATE operating_flight
                SET status = %s
                WHERE operating_airline_name = %s
                  AND flight_number = %s
            """, (status, airline_name, flight_number))

            conn.commit()
            message = "Flight status updated successfully."

        except Exception as e:
            print("OPERATOR ERROR:", e)
            conn.rollback()
            message = "Status update failed."

    cursor.execute("""
        SELECT
            flight_number,
            departure_port,
            arrival_port,
            departure_time,
            arrival_time,
            status
        FROM operating_flight
        WHERE operating_airline_name = %s
        ORDER BY departure_time
    """, (airline_name,))
    flights = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "airline_staff_page/airline_staff_operator.html",
        airline_name=airline_name,
        permissions=permissions,
        flights=flights,
        message=message
    )