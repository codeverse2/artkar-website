from flask import Flask, flash, redirect, request, render_template, render_template_string
import psycopg2

app = Flask(__name__)
app.secret_key = "super_secret_portfolio_key"

def get_db_connection():
    supabase_uri = "postgresql://postgres.ygtkibauxgbrknsuzjzb:coldhearted%407218@://supabase.com"
    return psycopg2.connect(supabase_uri)

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

def save_contact(name, email, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))
    conn.commit()
    cursor.close()
    conn.close()

def save_booking(name, email, phone, service, date, time, details):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO bookings (name, email, phone, service, date, time, details) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, email, phone, service, date, time, details))
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/contact", methods=["POST"])
def contact():
    save_contact(request.form["name"], request.form["email"], request.form["message"])
    flash("? Contact info saved successfully!")
    return redirect("/contact.html")

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
    flash("? Booking saved successfully!")
    return redirect("/booking.html")

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
        <h1>Portfolio Website Admin Dashboard ??</h1>
        <h2>Contact Form Submissions</h2>
        <table border="1">
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Message</th></tr>
            {% for row in contacts %}
            <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}</td></tr>
            {% endfor %}
        </table>
        <h2>Booking Sessions Requests</h2>
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
    app.run(debug=True)
