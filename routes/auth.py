import re
from datetime import datetime, date
from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


# ----------------------------
# Validation helper functions
# ----------------------------

def valid_phone(phone):
    return re.fullmatch(r"\+[0-9]{1,3}-[0-9]{2,4}-[0-9]{3,4}-[0-9]{4}", phone) is not None


def valid_passport(passport):
    return re.fullmatch(r"[A-Za-z0-9]{6,20}", passport) is not None


def valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def future_date(date_string):
    try:
        d = datetime.strptime(date_string, "%Y-%m-%d").date()
        return d > date.today()
    except ValueError:
        return False


# ----------------------------
# Register auth routes
# This function is called in app.py
# It attaches /register, /login, and /logout to the Flask app
# ----------------------------

def register_auth_routes(app, conn):

    # ----------------------------
    # Route: /register
    # Lets customer, booking agent, or airline staff create an account
    # ----------------------------
    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None

        cursor = conn.cursor(dictionary=True)

        # Load airlines for dropdown menus in register.html
        cursor.execute("""
            SELECT airline_name
            FROM airline
            ORDER BY airline_name
        """)
        airlines = cursor.fetchall()

        if request.method == "POST":
            user_type = request.form.get("user_type", "").strip()
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()

            if not user_type or not username or not password:
                cursor.close()
                return render_template(
                    "register.html",
                    error="Please fill in account type, username, and password.",
                    airlines=airlines
                )

            # hash pass using werkzeug
            password_hash = generate_password_hash(password)

            try:
                # ----------------------------
                # Register customer
                # ----------------------------
                if user_type == "customer":
                    name = request.form.get("name", "").strip()
                    building_number = request.form.get("building_number", "").strip()
                    street = request.form.get("street", "").strip()
                    city = request.form.get("city", "").strip()
                    state = request.form.get("state", "").strip().upper()
                    phone_number = request.form.get("phone_number", "").strip()
                    passport_number = request.form.get("passport_number", "").strip()
                    passport_expiration_date = request.form.get("passport_expiration_date", "").strip()
                    passport_country = request.form.get("passport_country", "").strip()
                    date_of_birth = request.form.get("customer_date_of_birth", "").strip()

                    if not name or not building_number or not street or not city or not state:
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Please fill in all customer address fields.",
                            airlines=airlines
                        )

                    if not valid_phone(phone_number):
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Phone number must look like +1-212-555-0101.",
                            airlines=airlines
                        )

                    if not valid_passport(passport_number):
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Passport number must be 6-20 letters/numbers.",
                            airlines=airlines
                        )

                    if not valid_date(passport_expiration_date):
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Passport expiration date must be valid.",
                            airlines=airlines
                        )

                    if not future_date(passport_expiration_date):
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Passport expiration date must be in the future.",
                            airlines=airlines
                        )

                    if not valid_date(date_of_birth):
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Date of birth must be valid.",
                            airlines=airlines
                        )

                    cursor.execute(
                        "SELECT customer_email FROM customer WHERE customer_email = %s",
                        (username,)
                    )
                    if cursor.fetchone():
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Customer email already exists.",
                            airlines=airlines
                        )

                    cursor.execute("""
                        INSERT INTO customer(
                            customer_email,
                            name,
                            password_hash,
                            building_number,
                            street,
                            city,
                            state,
                            phone_number,
                            passport_number,
                            passport_expiration_date,
                            passport_country,
                            date_of_birth
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        username,
                        name,
                        password_hash,
                        building_number,
                        street,
                        city,
                        state,
                        phone_number,
                        passport_number,
                        passport_expiration_date,
                        passport_country,
                        date_of_birth
                    ))

                # ----------------------------
                # Register booking agent
                # ----------------------------
                elif user_type == "booking_agent":
                    airline_name = request.form.get("agent_airline_name", "").strip()

                    if not airline_name:
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Booking agent must select airline name.",
                            airlines=airlines
                        )

                    cursor.execute(
                        "SELECT agent_email FROM booking_agent WHERE agent_email = %s",
                        (username,)
                    )
                    if cursor.fetchone():
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Booking agent email already exists.",
                            airlines=airlines
                        )

                    cursor.execute("""
                        INSERT INTO booking_agent(
                            agent_email,
                            password_hash,
                            airline_name
                        )
                        VALUES (%s, %s, %s)
                    """, (
                        username,
                        password_hash,
                        airline_name
                    ))

                # ----------------------------
                # Register airline staff
                # Staff key decides permission
                # 1234 = Admin
                # 5678 = Operator
                # ----------------------------
                elif user_type == "airline_staff":
                    first_name = request.form.get("first_name", "").strip()
                    last_name = request.form.get("last_name", "").strip()
                    date_of_birth = request.form.get("staff_date_of_birth", "").strip()
                    airline_name = request.form.get("staff_airline_name", "").strip()
                    staff_key = request.form.get("staff_key", "").strip()

                    if not first_name or not last_name or not date_of_birth or not airline_name or not staff_key:
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Airline staff must fill in all staff fields.",
                            airlines=airlines
                        )

                    if not valid_date(date_of_birth):
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Staff date of birth must be valid.",
                            airlines=airlines
                        )

                    if staff_key == "1234":
                        permission = "Admin"
                    elif staff_key == "5678":
                        permission = "Operator"
                    else:
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Invalid staff key.",
                            airlines=airlines
                        )

                    cursor.execute(
                        "SELECT staff_username FROM airline_staff WHERE staff_username = %s",
                        (username,)
                    )
                    if cursor.fetchone():
                        cursor.close()
                        return render_template(
                            "register.html",
                            error="Staff username already exists.",
                            airlines=airlines
                        )

                    cursor.execute("""
                        INSERT INTO airline_staff(
                            staff_username,
                            password_hash,
                            first_name,
                            last_name,
                            date_of_birth,
                            airline_name
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        username,
                        password_hash,
                        first_name,
                        last_name,
                        date_of_birth,
                        airline_name
                    ))

                    cursor.execute("""
                        INSERT INTO staff_permissions(
                            staff_username,
                            permission
                        )
                        VALUES (%s, %s)
                    """, (
                        username,
                        permission
                    ))

                else:
                    cursor.close()
                    return render_template(
                        "register.html",
                        error="Invalid user type.",
                        airlines=airlines
                    )

                conn.commit()
                cursor.close()
                return redirect(url_for("login"))

            except Exception as e:
                print("REGISTER ERROR:", e)
                conn.rollback()
                cursor.close()
                error = "Registration failed. Username may already exist, or airline name may be invalid."

        cursor.close()
        return render_template(
            "register.html",
            error=error,
            airlines=airlines
        )

    # ----------------------------
    # Route: /login
    # Logs users into the correct account type
    # Redirects already-logged-in users to their home page
    # ----------------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():

        if session.get("logged_in"):
            if session.get("user_type") == "customer":
                return redirect(url_for("customer.customer_home"))
            elif session.get("user_type") == "booking_agent":
                return redirect(url_for("booking_agent.booking_agent_home"))
            elif session.get("user_type") == "airline_staff":
                return redirect(url_for("airline_staff.airline_staff_home"))

        error = None

        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"].strip()
            user_type = request.form["user_type"]

            cursor = conn.cursor(dictionary=True)

            if user_type == "customer":
                query = """
                    SELECT customer_email AS username, password_hash
                    FROM customer
                    WHERE customer_email = %s
                """
            elif user_type == "booking_agent":
                query = """
                    SELECT agent_email AS username, password_hash
                    FROM booking_agent
                    WHERE agent_email = %s
                """
            elif user_type == "airline_staff":
                query = """
                    SELECT staff_username AS username, password_hash
                    FROM airline_staff
                    WHERE staff_username = %s
                """
            else:
                cursor.close()
                return render_template("login.html", error="Invalid user type.")

            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user["password_hash"], password):
                session["logged_in"] = True
                session["username"] = user["username"]
                session["user_type"] = user_type

                if user_type == "customer":
                    return redirect(url_for("customer.customer_home"))
                elif user_type == "booking_agent":
                    return redirect(url_for("booking_agent.booking_agent_home"))
                elif user_type == "airline_staff":
                    return redirect(url_for("airline_staff.airline_staff_home"))

            error = "Invalid username or password."

        return render_template("login.html", error=error)

    # ----------------------------
    # Route: /logout
    # Clears the session and sends user back to public home
    # ----------------------------
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))