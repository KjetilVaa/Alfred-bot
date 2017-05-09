import os, sys

from flask import Flask, request


app = Flask(__name__)

app.route("/", methods=["GET"])
def verify():
    #Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "alfred_success":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200


if __name__ == "__main__":
    app.run(debug=True, port=80)
