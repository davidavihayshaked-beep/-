import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

HOME_SERVER = "https://matrix.beeper.com"

# שלב 1: בקשת קוד מהמייל
@app.route('/step1/<email>')
def step1(email):
    res = requests.post(f"{HOME_SERVER}/_matrix/client/v3/login", 
                        json={"type":"m.login.email.identity", "identifier":{"type":"m.id.user", "user":email}})
    return "Check your email for a link/code from Beeper. After you click it, go to /step2/" + email

# שלב 2: קבלת ה-Token (תריץ את זה אחרי שאישרת במייל)
@app.route('/step2/<email>')
def step2(email):
    # אנחנו מנסים להתחבר שוב - אם אישרת במייל, השרת יחזיר לנו את ה-Token
    res = requests.post(f"{HOME_SERVER}/_matrix/client/v3/login", 
                        json={"type":"m.login.email.identity", "identifier":{"type":"m.id.user", "user":email}})
    data = res.json()
    token = data.get("access_token")
    if token:
        return f"YOUR_TOKEN: {token}"
    return f"Not authorized yet. Error: {data}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
