from typing import Any

from google.cloud import firestore
from models.enum import Decision


class HandleDecision:
    def __init__(self):
        self.db = firestore.Client()
        self.deciding_growth_limit = 0.09

    def _retrieve_calculated(self, battery_name: str) -> Any:
        return (
            self.db.collection("battery_actual")
            .document("calculated")
            .collection(str(battery_name))
            .order_by("chain_started", direction=firestore.Query.ASCENDING)
            .where(u"deprecated", u"==", False)
        )

    def _weekly_with_limit(
        self, average_growth_change_rate, last_stored, limit: int = 10
    ):
        print(average_growth_change_rate, last_stored)
        if (
            last_stored - (average_growth_change_rate * limit)
            > self.deciding_growth_limit
        ):
            return Decision.SAFE.format(weeks=limit)

        for x in reversed(range(limit - 1)):
            if (
                last_stored - (average_growth_change_rate * x + 1)
                <= self.deciding_growth_limit
            ):
                return Decision.UNSAFE.format(x + 1)
        return Decision.UNDETERMINED

    def decide(self, battery_name: str) -> object:
        calculated_stored = self._retrieve_calculated(battery_name).stream()

        arr = []
        last_stored = 0

        for doc in calculated_stored.stream():
            dicted = doc.to_dict()
            if arr:
                arr.append(float(last_stored - dicted["growth"]))
            last_stored = float(dicted["growth"])

        return self._weekly_with_limit((sum(arr) / len(arr)), last_stored)
