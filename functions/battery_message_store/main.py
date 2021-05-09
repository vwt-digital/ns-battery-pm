from utils import StoreDecide, filter_message, handle_message


def handle_battery_store(message):
    payload, _ = handle_message(message)

    for filtered, host, timestamp in filter_message(payload):
        print(f"{host}:{timestamp} Filtered message: {filtered}")
        store = StoreDecide()
        store.handle_store(filtered, host, timestamp)

    # Returning any 2xx status indicates successful receipt of the message.
    # 204: no content, delivery successful, no further actions needed
    return "OK", 204
