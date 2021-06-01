import json

import config
from gobits import Gobits


def publish(name, publisher):

    formatted = json.dumps(
        {"gobits": [Gobits().to_json()], "battery_name": name},
        indent=2,
    ).encode("utf-8")

    # Publish to ops-issues here
    topic_path = publisher.topic_path(config.PROJECT, config.TURN_TO_DECISION)
    publisher.publish(topic_path, formatted)
