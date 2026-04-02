from flask import Flask, render_template, request, redirect, session
import smtplib

app = Flask(__name__)
app.secret_key = "secret123"

# STORE INQUIRIES (temporary)
inquiries = []

# LOGIN DETAILS
USERNAME = "admin"
PASSWORD = "admin123"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        message = request.form["message"]

        # SAVE INQUIRY
        inquiries.append({
            "name": name,
            "phone": phone,
            "message": message
        })

        # EMAIL SEND
        sender_email = "vaishnavinirpal8@gmail.com"
        app_password = "YOUR_APP_PASSWORD"

        receiver_email = "vaishnavinirpal8@gmail.com"

        subject = "New Inquiry"
        body = f"Name: {name}\nPhone: {phone}\nMessage: {message}"

        email_text = f"Subject: {subject}\n\n{body}"

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, email_text)
            server.quit()
        except:
            print("Email failed")

        return render_template("index.html", success=True)

    return render_template("index.html")


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")


# ADMIN DASHBOARD
@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")

    return render_template("admin.html", inquiries=inquiries)


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)