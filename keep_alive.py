from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "PhantomScalerX v7.1 – Alert + Hype Engine Running"

def keep_alive():
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()