from utils import HandleCalculate, handle_message


def handle_calculate_store(message):

    payload, _ = handle_message(message)

    for r_chain_instance in payload:
        handle = HandleCalculate()
        del handle
        # handle.calculate_overall_growth(r_chain_instance)
    # Returning any 2xx status indicates successful receipt of the message.
    # 204: no content, delivery successful, no further actions needed
    return "OK", 204
