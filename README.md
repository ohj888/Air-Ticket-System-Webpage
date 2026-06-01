# Air Ticket System Webpage

This project is a simple air ticket system web application. It includes a front end connected to a back-end database. The database is managed through MySQL/phpMyAdmin.

The website runs using Flask. The Flask app connects the HTML pages, routing logic, login system, and database queries together.

## Main Features

* Front-end webpage for an air ticket system
* Back-end database connection using MySQL
* Flask-based web server
* Login and session checks
* Basic secure password management using werkzeug security
* Separate route files for different website functions
* HTML templates for the user interface
* SQL insert files for setting up database records

## Project Structure

```text
part3/
├── app.py
├── db.py
├── routes/
├── templates/
├── static/
├── sql_supplementary/
└── README.md
```

## File Overview

`app.py` is the main Flask application file. It starts the website and connects the different route files.

`db.py` contains the database connection setup.

`routes/` contains the different Flask routes for the website, such as login, customer pages, booking agent pages, and other webpage functions.

`templates/` contains the HTML pages used by Flask to render the website.

`static/` contains static files such as images, CSS, and JavaScript.

`sql_supplementary/` contains SQL insert files used to add data into the database.

## Notes

This project was built as a database-backed web application. It demonstrates how a front end can connect to a back-end database through Flask routes and SQL queries.
