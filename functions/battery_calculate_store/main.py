from google.cloud import pubsub_v1
from utils import HandleCalculate, handle_message, publish


def handle_calculate_store(message):
    publisher = pubsub_v1.PublisherClient()

    payload, _ = handle_message(message)
    handle_calculate = HandleCalculate()

    chain = handle_calculate.create_chain(payload["chain_name"])
    handle_calculate.store_calculated(
        chain, handle_calculate.calculate_overall_growth(chain)
    )
    publish(chain.name, publisher)

    # Returning any 2xx status indicates successful receipt of the message.
    # 204: no content, delivery successful, no further actions needed
    return "OK", 204
