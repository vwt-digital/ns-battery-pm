from datetime import datetime

from google.cloud import firestore
from models.enum import Decision


class HandleDecision:
    def __init__(self):
        self.db = firestore.Client()
        self.deciding_growth_limit = 0.001

    def _retrieve_calculated(self, battery_name: str):
        return (
            self.db.collection("battery_actual")
            .document("calculated")
            .collection(str(battery_name))
            .order_by("chain_started", direction=firestore.Query.ASCENDING)
        )

    def _weekly_with_limit(
        self, average_growth_change_rate, last_stored, limit: int = 10
    ):
        print(average_growth_change_rate, last_stored, limit)
        if (
            last_stored - (average_growth_change_rate * limit)
            > self.deciding_growth_limit
        ):
            return Decision.SAFE.value.format(weeks=limit)

        for x in range(limit):
            if (
                last_stored - (average_growth_change_rate * (x + 1))
                <= self.deciding_growth_limit
            ):
                return Decision.UNSAFE.value.format(weeks=x + 1)
        return Decision.UNDETERMINED.value

    def store(self, battery_name, decision):
        self.db.collection("battery_actual").document("decision").collection(
            str(battery_name)
        ).document(str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))).set(
            {"decision": str(decision)}
        )

    def decide(self, battery_name: str) -> object:
        calculated_stored = self._retrieve_calculated(battery_name).stream()
        arr = []
        last_stored = None

        for doc in calculated_stored:
            dicted = doc.to_dict()
            if dicted["deprecated"]:
                continue
            if not (last_stored is None):
                arr.append(float(float(last_stored) - float(dicted["growth"])))
            last_stored = float(dicted["growth"])

        if not arr:
            return Decision.UNDETERMINED.value

        return self._weekly_with_limit((sum(arr) / len(arr)), last_stored)
