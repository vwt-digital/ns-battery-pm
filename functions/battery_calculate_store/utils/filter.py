import base64
import json


def handle_message(message):
    envelope = json.loads(message.data.decode("utf-8"))
    return json.loads(base64.b64decode(envelope["message"]["data"])), envelope
