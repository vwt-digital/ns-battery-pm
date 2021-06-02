from utils import HandleDecision, handle_message


def handle_decision(message):
    payload, _ = handle_message(message)
    handle_decision = HandleDecision()

    handle_decision.store(
        payload["battery_name"], handle_decision.decide(payload["battery_name"])
    )

    # Returning any 2xx status indicates successful receipt of the message.
    # 204: no content, delivery successful, no further actions needed
    return "OK", 204
