import mysql.connector
from flask import Flask, render_template, request, abort, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

# Imports form routes
from routes.customer import customer_bp
from routes.auth import register_auth_routes
from routes.booking_agent import booking_agent_bp
from routes.airline_staff import airline_staff_bp
from db import get_db_connection

# --------

# -------- USE THIS LINK TO OPEN -------- #
# http://127.0.0.1:5000 
# -------- USE THIS LINK TO OPEN -------- #

# create flask object
app = Flask(__name__)

# secret key

app.secret_key = '123abc'

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "Air_Ticket" 
)

# register login page --------
register_auth_routes(app, conn)
# --------



# create safety list of table names so that 
# users cannot type random table name into url 
ALLOWED_TABLES = [
    "aircraft",
    "airline",
    "airline_staff",
    "airport",
    "booking_agent",
    "booking_agent_purchases",
    "customer",
    "customer_purchases",
    "marketing_flight",
    "operating_flight",
    "staff_permissions",
    "ticket"
]

# route for home page
# when the user visits http://127.0.0.1:5000/
# flask runs this
@app.route("/")
def index():
    # render index.html and send allowed tables to page
    # html can loop throuhg tables and display
    return render_template("index.html", tables = ALLOWED_TABLES)

# route for showign one table --------
# EX: /table/airport gives table_name = "airport"
@app.route("/table/<table_name>")
def show_table(table_name):

    # check if table is in allowed tables
    if table_name not in ALLOWED_TABLES:
        abort(404)

    # create local database connection
    local_conn = get_db_connection()

    # create cursor that lets us run sql and get rows back
    # dict = true makes all returned rows as a dictionary
    cursor = local_conn.cursor(dictionary = True, buffered = True)   

    # select all query
    query = f"SELECT * FROM `{table_name}`"

    # send query to mysql
    cursor.execute(query)

    # fetch all returned rows from query
    # rows as list of dict
    rows = cursor.fetchall()

    # close cursor 
    cursor.close()

    # close local database connection
    local_conn.close()

    # rows[0].keys() gives dict keys (which are col names)
    # if no rows empty list
    columns = rows[0].keys() if rows else []

    # render table.html and send
    return render_template(
        "table.html",
        table_name = table_name,
        columns = columns,
        rows = rows
    )
# --------



# get inprogress flights --------
@app.route("/get_in_progress_flights")
def get_in_progress_flights():
    marketing_airline_name = request.args.get("marketing_airline_name")

    # create local database connection
    local_conn = get_db_connection()

    cursor = local_conn.cursor(dictionary=True, buffered=True)

    query = """
        SELECT
            mf.marketing_airline_name,
            mf.marketing_flight_num,
            ofl.operating_airline_name,
            ofl.flight_number
        FROM marketing_flight mf
        JOIN operating_flight ofl
            ON mf.operating_airline_name = ofl.operating_airline_name
           AND mf.flight_number = ofl.flight_number
        WHERE mf.marketing_airline_name = %s
          AND ofl.status = 'in-progress' 
        ORDER BY mf.marketing_flight_num
    """

    cursor.execute(query, (marketing_airline_name,))
    flights = cursor.fetchall()
    cursor.close()
    local_conn.close()

    return jsonify({"flights": flights})

# --------



# new route for searching airport --------
@app.route("/search_airport", methods=["GET", "POST"])
def search_airport():
    rows = []      # store query results
    columns = []   #  store inputs from html form
    message = ""

    # create local database connection
    local_conn = get_db_connection()

    cursor = local_conn.cursor(dictionary=True, buffered=True)

    cursor.execute("""
                   Select airport_name, city 
                   from airport
                   order by city, airport_name"""
                   )
    airports = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT marketing_airline_name
        FROM marketing_flight
        ORDER BY marketing_airline_name
    """)
    marketing_airlines = cursor.fetchall()

    cursor.close()

    if request.method == "POST":

        # gets what kind of search is being preformed
        search_type = request.form['search_type']

        cursor = local_conn.cursor(dictionary = True, buffered = True)

        # case 1 public user searches upcoming
        if search_type == 'upcoming':
            # fill in valus from html
            
            origin = request.form['origin'].strip()
            destination = request.form['destination'].strip()
            date = request.form['date'].strip()

            if not origin or not destination:
                message = 'Please select origin and destination.'

            elif origin == destination:
                message = 'Origin and Destination Must be Different'

            else:
                query = """
                    SELECT 
                        ofl.departure_port,
                        ofl.arrival_port,
                        mf.marketing_airline_name as marketing_airline,
                        mf.marketing_flight_num as marketing_code,
                        ofl.operating_airline_name as operating_flight,
                        ofl.flight_number AS operating_code,
                        ofl.departure_time,
                        ofl.arrival_time,
                        ofl.price,
                        ofl.status
                    FROM marketing_flight mf
                    JOIN operating_flight ofl 
                        ON mf.operating_airline_name = ofl.operating_airline_name
                    AND mf.flight_number = ofl.flight_number
                    WHERE ofl.status IN ('upcoming', 'delayed')
                    AND ofl.departure_port = %s
                    AND ofl.arrival_port = %s
                """

                params = [origin, destination]

                if date:
                    query += " AND DATE(ofl.departure_time) = %s"
                    params.append(date)

                query += " ORDER BY ofl.departure_time"

                try:
                    cursor.execute(query, params)
                    rows = cursor.fetchall()

                    if rows: 
                        columns = rows[0].keys()
                    else:
                        columns = []
                        message = 'No Flights Found'
                    
                except Exception as e:
                    print("SQL ERROR: ", e)
                    rows = []
                    columns = []
                    message = 'search error'
                finally:
                    cursor.close()

        elif search_type == 'status':
            marketing_airline_name = request.form['marketing_airline_name'].strip()
            marketing_flight_num = request.form['marketing_flight_num'].strip()

            # if marketing airline name and number not equal to operating name/number then its 
            # a code share and we add the operating flight info
            query = """
                SELECT
                    mf.marketing_airline_name AS marketing_airline,
                    mf.marketing_flight_num AS marketing_code,nano ~/.ssh/config

                    CASE
                        WHEN mf.marketing_airline_name <> ofl.operating_airline_name
                        OR mf.marketing_flight_num <> ofl.flight_number
                        THEN ofl.operating_airline_name
                        ELSE NULL
                    END AS operating_airline,

                    CASE
                        WHEN mf.marketing_airline_name <> ofl.operating_airline_name
                        OR mf.marketing_flight_num <> ofl.flight_number
                        THEN ofl.flight_number
                        ELSE NULL
                    END AS operating_code,

                    CASE
                        WHEN mf.marketing_airline_name <> ofl.operating_airline_name
                        OR mf.marketing_flight_num <> ofl.flight_number
                        THEN 'Yes'
                        ELSE 'No'
                    END AS code_share,

                    ofl.departure_port,
                    ofl.arrival_port,
                    ofl.departure_time,
                    ofl.arrival_time,
                    ofl.price,
                    ofl.status
                FROM marketing_flight mf
                JOIN operating_flight ofl
                    ON mf.operating_airline_name = ofl.operating_airline_name
                AND mf.flight_number = ofl.flight_number
                WHERE mf.marketing_airline_name = %s
                AND mf.marketing_flight_num = %s
                And ofl.status='in-progress'
            """

            try: 
                cursor.execute(query, (marketing_airline_name, marketing_flight_num))
                rows = cursor.fetchall()

                if rows:
                    columns = rows[0].keys()
                else:
                    columns = []
                    message = "No flight found."
            except Exception as e:
                print("SQL Error: ", e)
                rows = []
                columns = []
                message = 'search error'
            finally:
                cursor.close()

    # close local database connection
    local_conn.close()

    return render_template(
        "search_airport.html",
        rows = rows,
        columns = columns,
        message = message,
        airports = airports,
        marketing_airlines = marketing_airlines,
        )


# --------

# Customer homepage --------
app.register_blueprint(customer_bp)
# --------

# booking agent page --------
app.register_blueprint(booking_agent_bp)
# --------



# airline staff homepage --------
app.register_blueprint(airline_staff_bp)
# --------

# This part makes sure the app runs only when this file is executed directly
# debug=True means Flask auto-restarts when you save changes
# It also shows clearer error messages while developing
if __name__ == "__main__":
    app.run(debug=True)