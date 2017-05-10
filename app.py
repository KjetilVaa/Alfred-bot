import os, sys
from captureWebCamPicture import takePicture
from flask import Flask, request, send_file
from threading import Timer
import requests
from pymessenger import Bot


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAADyBpRsToMBAA38IirkkrfZCyk7CD9C7eN6GWdTK0yCg7n19k2XewzM9uAuTNvDlzZBl5CaCQfZCByUYctDzNVz81bDQmCNZA9cfNAHh88mkeaeMUQZCljwnuYdZAEsPxNBx37xImpdUYZA5FTUYEkNzwbZBg67JtzZC6AypPiMY7QZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)
imageurl = "https://5d8f1f5d.eu.ngrok.io/bilde.png"


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "alfred_success":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Nonnegata", 200


@app.route("/bilde.png", methods=["GET"])
	#Getting image
def sendImage():
	return send_file("bilde.png", mimetype="image/png"), 200



@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

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


					response = messaging_text
					# Echo
					if messaging_text == "Picture" or messaging_text == "picture":
						bot.send_message("Taking picture...")
						takePicture()
						print("sending picture")
						#bot.send_image_url(sender_id, imageurl)
						t = Timer(10.0, sendPictureJson("https://5d8f1f5d.eu.ngrok.io/bilde.png", sender_id))
						t.start()

					#bot.send_text_message(sender_id, response)

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
					"template_type" : "generic",
					"elements": [{
						"title":"Nonnegata stue",
						"image_url": url
					}]
				}
			}
		}
	}

	params = {
		"access_token": PAGE_ACCESS_TOKEN
	}

	r = requests.post("https://graph.facebook.com/v2.6/me/messages",json=json_data, params=params)
	print(r, r.status_code, r.text)





if __name__ == "__main__":
	app.run(debug = True, port = 80)


