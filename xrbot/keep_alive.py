from threading import Thread
from flask import Flask

# To keep the bot online 24/7

app = Flask("")


@app.route("/")
def home():
    """_summary_

    Returns:
            _type_: _description_
    """
    return ""


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
