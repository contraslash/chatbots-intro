import conf
import requests
from sanic import Sanic
from sanic.response import (
    json as sanic_json,
    text as sanic_text
)
# We want to access parent folder projects
import sys
sys.path.append('..')

import rasa

app = Sanic(__name__)


@app.route("/facebook", methods=['GET', 'POST'])
def facebook(request):
    print(request.json)
    print(request.raw_args)
    if request.raw_args.get("hub.mode", "") == "subscribe":
        if request.raw_args.get(
            "hub.verify_token",
            ""
        ) == conf.FB_VERIFY_TOKEN:
            print("Token Match")
            return sanic_text(request.raw_args.get("hub.challenge", ""))
        else:
            print("Token DOES NOT Match")
            return sanic_text("Forbidden", status=403)
    if request.json.get("object", "") == "page":
        body = request.json
        for entry in body["entry"]:
            for messaging in entry['messaging']:
                if messaging.get('message', ""):
                    print("Menssage:", messaging['message'])
                    raw_text = messaging['message']['text']
                    entities, intent = rasa.extration_and_classification(
                        raw_text
                    )
                    response = rasa.production(intent, entities)
                    send_response(messaging['sender'], response)

    return sanic_text("")


def send_response(sender_object, response):
    data = dict()
    data['recipient'] = sender_object
    data['message'] = {
        'text': response
    }

    query_params = {
        'access_token': conf.FB_TOKEN
    }

    response = requests.post(
        conf.FB_MESSENGER_URL,
        params=query_params,
        json=data
    )

    print(response.status_code, response.content)


if __name__ == '__main__':
    rasa.configure()
    app.run(host="0.0.0.0", port=5000, debug=True)
