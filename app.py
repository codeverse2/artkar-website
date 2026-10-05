from flask import Flask, flash, redirect, request, render_template, render_template_string
import psycopg2
import os

app = Flask(__name__)
# ✅ Use environment variable for secret key, fallback to hardcoded string
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_portfolio_key")

# ✅ Database connection helper
def get_db_connection():
    # Look for DATABASE_URL environment variable (set in Vercel)
    db_url = os.environ.get("DATABASE_URL")

    # Fallback if not set (local testing only)
    if not db_url:
        db_url = "postgresql://postgres:coldhearted7218@db.ygtkibauxgbrknsuzjzb.supabase.co:5432/postgres"

    return psycopg2.connect(db_url)

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/gallery.html")
def gallery():
    return render_template("gallery.html")

@app.route("/contact.html")
def contact_page():
    return render_template("contact.html")

@app.route("/booking.html")
def booking_page():
    return render_template("booking.html")

# Save contact form data
def save_contact(name, email, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Save booking form data
def save_booking(name, email, phone, service, date, time, details):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (name, email, phone, service, date, time, details) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, email, phone, service, date, time, details)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Contact form submission
@app.route("/contact", methods=["POST"])
def contact():
    save_contact(request.form["name"], request.form["email"], request.form["message"])
    flash("✅ Contact info saved successfully!")
    return redirect("/contact.html")

# Booking form submission
@app.route("/booking", methods=["POST"])
def booking():
    save_booking(
        request.form["name"],
        request.form["email"],
        request.form.get("phone", ""),
        request.form["service"],
        request.form["date"],
        request.form.get("time", ""),
        request.form["message"]
    )
    flash("✅ Booking saved successfully!")
    return redirect("/booking.html")

# Admin dashboard
@app.route("/admin")
def view_admin_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts_data = cursor.fetchall()
    cursor.execute("SELECT * FROM bookings")
    bookings_data = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """
    <html>
    <head><title>Admin Dashboard</title></head>
    <body>
        <h1>Portfolio Website Admin Dashboard ✅</h1>

        <h2>Contact Form Submissions</h2>
        <table border="1">
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Message</th></tr>
            {% for row in contacts %}
            <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}</td></tr>
            {% endfor %}
        </table>

        <h2>Booking Session Requests</h2>
        <table border="1">
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Service</th><th>Date</th><th>Time</th><th>Details</th></tr>
            {% for row in bookings %}
            <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}</td><td>{{ row[4] }}</td><td>{{ row[5] }}</td><td>{{ row[6] }}</td><td>{{ row[7] }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, contacts=contacts_data, bookings=bookings_data)

if __name__ == "__main__":
    # ✅ Use host/port for Vercel compatibility
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
