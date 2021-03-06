from google.cloud import pubsub_v1
from utils import StoreDecide, filter_message, handle_message, publish


def handle_battery_store(message):
    """

    :param message:
    :return:
    """
    publisher = pubsub_v1.PublisherClient()

    payload, _ = handle_message(message)

    store = StoreDecide()
    # Filter based on a yield return, to speed up process as researched in 7.1
    for filtered, host, timestamp in filter_message(payload):
        battery, should_publish = store.handle_store(filtered, host, timestamp)

        if should_publish:  # (has_chain and battery.actual >= 100)
            publish(battery.battery_hg_name, publisher)

    # Returning any 2xx status indicates successful receipt of the message.
    # 204: no content, delivery successful, no further actions needed
    return "OK", 204
