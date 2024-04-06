from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, emit
from google.oauth2 import id_token
from google.auth.transport import requests
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()
socketio = SocketIO(app,cors_allowed_origins="*")
button_presses = {}

@app.route("/login")
def login():
    return render_template("flask_sockets_login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        try:
            token = request.form["credential"]
            id_info = id_token.verify_oauth2_token(token, requests.Request(), "665033402801-airrnnu2n9d85qec4ue0kuh4dn9d9a1f.apps.googleusercontent.com")
            session["user_id"] = id_info["sub"]
            if not(id_info["sub"] in button_presses):
                button_presses[id_info["sub"]] = 0
        except ValueError:
            redirect(url_for("login"))

    if session.get("user_id"):
        return render_template("flask_sockets_dashboard.html")
    return redirect(url_for("login"))

@socketio.on("value_update")
def value_update(data):
    global button_presses
    button_presses[session["user_id"]] += data["value"]
    emit("button_click_response", {"value": button_presses[session["user_id"]]})

if __name__ == '__main__':
    socketio.run(app)
