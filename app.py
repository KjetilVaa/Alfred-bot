import os, sys
from captureWebCamPicture import takePicture
from flask import Flask, request, send_file
import requests
import random
from pymessenger import Bot
from textToSpeech import say

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAADyBpRsToMBAA38IirkkrfZCyk7CD9C7eN6GWdTK0yCg7n19k2XewzM9uAuTNvDlzZBl5CaCQfZCByUYctDzNVz81bDQmCNZA9cfNAHh88mkeaeMUQZCljwnuYdZAEsPxNBx37xImpdUYZA5FTUYEkNzwbZBg67JtzZC6AypPiMY7QZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)
imageurl = "https://5d8f1f5d.eu.ngrok.io/bilde.png"


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "alfred_success":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Nonnegata", 200


@app.route("/bilde.png/<int:id>", methods=["GET"])
# Getting image
def sendImage(id):
    a = takePicture()
    return send_file(a, mimetype="image/png"), 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    print(messaging_text)
                    print(messaging_text[:4])
                    print(messaging_text[4:])

                    # Echo
                    if messaging_text == "Picture" or messaging_text == "picture":
                        bot.send_message(sender_id, "Taking picture...")
                        print("sending picture")
                        a = random.randint(0, 1000)
                        # bot.send_image_url(sender_id, imageurl)
                        sendPictureJson("https://5d8f1f5d.eu.ngrok.io/bilde.png/" + str(a), sender_id)
                        # bot.send_text_message(sender_id, response)
                    elif "Say" in messaging_text or "say" in messaging_text:
                        print("speak")
                        text = messaging_text[4:]
                        say(text)
                        bot.send_text_message(sender_id, "Saying: " + text)
                    else:
                        bot.send_text_message(sender_id, "No command found, sir.")

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


def sendPictureJson(url, senderid):
    json_data = {
        "recipient": {"id": senderid},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Nonnegata stue",
                        "image_url": url
                    }]
                }
            }
        }
    }

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", json=json_data, params=params)
    print(r, r.status_code, r.text)


if __name__ == "__main__":
    app.run(debug=True, port=80)
