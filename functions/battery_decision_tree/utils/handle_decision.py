from typing import Any

from google.cloud import firestore


class HandleDecision:
    def __init__(self):
        self.db = firestore.Client()

    def retrieve_calculated(self, battery_name: str) -> Any:
        return (
            self.db.collection("battery_actual")
            .document("calculated")
            .collection(str(battery_name))
        )

    def decide(self, battery_name: str) -> object:
        calculated_growth_stored = self.retrieve_calculated(battery_name)
        for doc in calculated_growth_stored.stream():
            print(f"{doc.id} => {doc.to_dict()}")

        return {}
