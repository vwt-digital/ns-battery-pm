from battery_actual import BatteryActual
from google.cloud import firestore


class StoreDecide:
    def __init__(self):
        self.db = firestore.Client()

    def handle_store(self, message, host, timestamp):
        """
            Handles the store functionality. Will take in the battery and retrieve its chains.
            If no chain exists, but the battery actual is lower than 100, it will create a new chain.
            If a chain does exist and the battery actual is lower than 100, it will add to that chain. If the battery actual \
            is 100, but the last chain instance was lower, it will add to that chain and ask for a message to be published.
        """
        battery = (
            BatteryActual.from_dict(message).add_timestamp(timestamp).add_host(host)
        )
        chain, has_chain = self.__retrieve_chain(battery)

        if not has_chain and battery.actual < 100:
            chain = chain.document(str(timestamp))
            chain.set({"chain_started": str(timestamp), "deprecated": False})
            chain = chain.collection("collected")

        if has_chain or (not has_chain and battery.actual < 100):
            chain.document(str(timestamp)).set(battery.to_dict())

        return battery, (has_chain and battery.actual >= 100)

    def __retrieve_chain(self, battery):
        """
        :param battery:
        :return:
        """
        battery_collection = (
            self.db.collection("battery_actual")
                .document("chains")
                .collection(str(battery.battery_hg_name))
        )

        try:
            # Retrieve the last chain that was created, based on a key in the document called chain_started.
            latest_chain = battery_collection.document(
                [
                    x.id
                    for x in battery_collection.order_by(
                    "chain_started", direction=firestore.Query.DESCENDING
                )
                    .limit(1)
                    .stream()
                ][0]
            ).collection("collected")

            # Retrieve the last instance based on the collected key.
            latest_collected = latest_chain.document(
                [
                    x.id
                    for x in latest_chain.order_by(
                    "collected", direction=firestore.Query.DESCENDING
                )
                    .limit(1)
                    .stream()
                ][0]
            )
            # Chain exists, so it will return the chain from the last chain retrieved.
            if latest_collected.get().to_dict()["actual"] < 100:
                return latest_chain, True
        except IndexError:
            pass
        # No battery actual is present in the latest chain that is lower than 100, so it will pass a new created chain with \
        # the right name (battery_hg_name
        return battery_collection, False
