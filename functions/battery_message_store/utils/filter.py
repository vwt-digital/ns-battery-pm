import base64
import json

import config


def handle_message(message):
    envelope = json.loads(message.data.decode("utf-8"))
    return json.loads(base64.b64decode(envelope["message"]["data"])), envelope


def filter_message(message):
    for performance in message[config.STORE_PERFORMANCE_KEY]:
        host = performance["hostName"]
        for nested_data in performance["performanceData"]:
            if nested_data["var_name"] == "battery_capacity":
                yield nested_data, host, performance["timestamp"]
