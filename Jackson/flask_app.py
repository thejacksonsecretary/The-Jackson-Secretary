from flask import Flask, render_template, session, redirect, url_for, request
from google.oauth2 import id_token
from google.auth.transport import requests
import secrets
from datetime import timedelta
import GeminiPrompting as gi

app = Flask(__name__)
app.secret_key = secrets.token_hex()
app.permanent_session_lifetime = timedelta(minutes = 5)
inputs = {}

@app.route("/")
def home():

    """Redirects to dashboard if signed in, if not redirects to login"""

    return redirect(url_for("main"))

@app.route("/logout")
def logout():

    """Clear session and redirect to sign in page"""

    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("pfp", None)
    return redirect(url_for("login"))

@app.route("/login")
def login():

    """Renders login page"""

    return render_template("login.html")

@app.route("/response", methods=["GET", "POST"])
def response():

    """Renders response page"""

    if not(session.get("user_id") and session.get("username") and session.get("pfp")):
        return redirect(url_for("login"))

    past_input = "._."
    response = "Request not recieved"
    if request.method == "POST" and "input" in request.form:
        past_input = request.form["input"]
        response = gi.prompt(past_input, session.get("user_id"))

    return render_template("response.html", inp = past_input, response = response, username = session["username"], pfp_url = session["pfp"])

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html")

def parse(calendar):
    eventString = ""
    for i in range(len(calendar)):
        name = calendar[i][0]
        dateStart = calendar[i][1][:10] + " " + calendar[i][1][10:]
        dateEnd = calendar[i][2][:10] + " " + calendar[i][2][10:]
        eventString += f"• {dateStart} to {dateEnd}: {name}\n"
    if eventString == "":
        return "No events!"
    return eventString

@app.route("/calendar")
def handle_error():

    """Return calendar page"""
    if not(session.get("user_id") and session.get("username") and session.get("pfp")):
        return redirect(url_for("login"))

    return render_template("calendar.html", username = session["username"], pfp_url = session["pfp"], calendar_events = parse(gi.dumpTruck(session["user_id"])))

@app.route("/main", methods=["GET", "POST"])
def main():

    global inputs

    """Renders dashboard"""

    if request.method == "POST" and "credential" in request.form:

        try:
            token = request.form["credential"]
            id_info = id_token.verify_oauth2_token(token, requests.Request(), "665033402801-0bb1erkdpbvp2act2pq4flkattrukfj6.apps.googleusercontent.com")
            session["user_id"] = id_info["sub"]
            session["username"] = id_info["name"]
            session["pfp"] = id_info["picture"]
            if not(id_info["sub"] in inputs):
                inputs[id_info["sub"]] = ""
        except ValueError:
            redirect(url_for("login"))

    if session.get("user_id") and session.get("username") and session.get("pfp"):
        return render_template("main.html", username = session["username"], pfp_url = session["pfp"])
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run()
