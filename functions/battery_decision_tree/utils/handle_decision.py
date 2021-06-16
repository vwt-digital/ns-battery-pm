from datetime import datetime

from google.cloud import firestore
from models.enum import Advice


class HandleDecision:
    def __init__(self):
        self.db = firestore.Client()
        self.deciding_growth_limit = 0.001

    def __retrieve_calculated(self, battery_name: str):
        return (
            self.db.collection("battery_actual")
            .document("calculated")
            .collection(str(battery_name))
            .order_by("chain_started", direction=firestore.Query.ASCENDING)
        )

    def __weekly_with_limit(
        self, average_growth_change_rate, last_stored, limit: int = 10
    ):
        if (
            last_stored - (average_growth_change_rate * limit)
            > self.deciding_growth_limit
        ):
            return Advice.SAFE.value.format(weeks=limit)

        for x in range(limit):
            if (
                last_stored - (average_growth_change_rate * (x + 1))
                <= self.deciding_growth_limit
            ):
                return Advice.UNSAFE.value.format(weeks=x + 1)
        return Advice.UNDETERMINED.value

    def __deprecate_calculated(self, battery_name, doc_id):
        doc = (
            self.db.collection("battery_actual")
            .document("calculated")
            .collection(str(battery_name))
            .document(doc_id)
        )
        doc.set({"deprecated": True})

    def __delete_calculated(self, battery_name, doc_id):
        self.db.collection("battery_actual").document("calculated").collection(
            str(battery_name)
        ).document(doc_id).delete()

    def store(self, battery_name, decision):
        self.db.collection("battery_actual").document("decision").collection(
            str(battery_name)
        ).document(str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))).set(
            {"decision": str(decision)}
        )

    def decide(self, battery_name: str) -> object:
        calculated_stored = self.__retrieve_calculated(battery_name)
        arr = []
        last_stored = None

        for doc in calculated_stored.stream():
            dicted = doc.to_dict()
            if dicted["deprecated"]:
                if (
                    datetime.strptime(dicted["chain_started"], "%Y-%m-%dT%H:%M:%SZ")
                    - datetime.now()
                ).days >= 15:
                    self.__delete_calculated(battery_name, doc.id)
                continue
            if not (last_stored is None):
                cal = float(float(last_stored) - float(dicted["growth"]))
                if cal < 0:
                    self.__deprecate_calculated(battery_name, doc.id)
                    continue
                arr.append(cal)
            last_stored = float(dicted["growth"])

        if not arr:
            return Advice.UNDETERMINED.value

        return self.__weekly_with_limit((sum(arr) / len(arr)), last_stored)
