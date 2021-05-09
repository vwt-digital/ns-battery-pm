from battery import Battery
from google.cloud import firestore


class StoreDecide:
    def __init__(self):
        self.db = firestore.Client()

    def handle_store(self, message, host, timestamp):

        battery = Battery.from_dict(message).add_timestamp(timestamp).add_host(host)
        chain, has_chain = self.retrieve_chain(battery)

        if not has_chain and battery.actual < 100:
            chain = chain.document(str(timestamp))
            chain.set({"chain_started": str(timestamp)})
            chain = chain.collection("collected")

        if has_chain or (not has_chain and battery.actual < 100):
            chain.document(str(timestamp)).set(battery.to_dict())

    def retrieve_chain(self, battery):
        battery_collection = (
            self.db.collection("battery_actual")
            .document("chains")
            .collection(str(battery.battery_hg_name))
        )

        try:
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
            print(f"Last collected: {latest_collected.get().to_dict()}")
            if latest_collected.get().to_dict()["actual"] < 100:
                return latest_chain, True
        except IndexError:
            pass

        return battery_collection, False
