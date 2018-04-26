from flask import Flask, request
from steemconnect.client import Client

app = Flask(__name__)


client_id = "your.app"
client_secret = "your_secret"

c = Client(client_id=client_id, client_secret=client_secret)


@app.route('/')
def index():
    login_url = c.get_login_url(
        "http://localhost:5000/welcome",
        "login",
    )
    return "<a href='%s'>Login with SteemConnect</a>" % login_url


@app.route('/welcome')
def welcome():
    c.access_token = request.args.get("access_token")
    return "Welcome <strong>%s</strong>!" % c.me()["name"]