from datetime import datetime
from typing import Type

from google.cloud import firestore
from models.chain import Chain
from models.chain_instance import ChainInstance


class HandleCalculate:
    def __init__(self):
        self.db = firestore.Client()

    @staticmethod
    def calculate_overall_growth(chain: Chain):
        """
        Calculate overall growth. Take chain difference and see the difference in percentage between one minute
        :param chain:
        """
        diff_list = []

        prev_instance = None
        instance: Type[ChainInstance]

        for instance in chain.chain_instances:
            if prev_instance and prev_instance.actual <= instance.actual:
                between_dates_s = (
                    datetime.strptime(instance.placed, "%Y-%m-%dT%H:%M:%SZ")
                    - datetime.strptime(prev_instance.placed, "%Y-%m-%dT%H:%M:%SZ")
                ).total_seconds()
                r_difference = (
                    instance.actual - prev_instance.actual
                ) / prev_instance.actual
                diff_list.append((r_difference / between_dates_s) * 60)
            prev_instance = instance

        return float(sum(diff_list)) / float(len(diff_list))

    @staticmethod
    def calculate_fast_growth(chain: Chain):
        return NotImplemented

    @staticmethod
    def calculate_drip_growth(chain: Chain):
        return NotImplemented

    @staticmethod
    def should_store(chain: Chain):
        return NotImplemented

    @staticmethod
    def prob_is_replaced(chain: Chain):
        return NotImplemented

    def remove_chain(self, chain: Chain):
        self.db.collection("battery_actual").document("chains").collection(
            chain.name
        ).document(chain.collected).delete()

    def create_chain(self, chain_name: str) -> Chain:
        battery_collection = (
            self.db.collection("battery_actual")
            .document("chains")
            .collection(str(chain_name))
        )
        r_chain = battery_collection.document(
            [
                x.id
                for x in battery_collection.order_by(
                    "chain_started", direction=firestore.Query.DESCENDING
                )
                .limit(1)
                .stream()
            ][0]
        )
        chain = Chain.from_dict({"collected": r_chain.id, "name": chain_name})

        for instance in r_chain.collection("collected").stream():
            chain.add_chain_instance(ChainInstance.from_dict(instance.to_dict()))

        return chain.sort_chain_on_placed()

    def store_calculated(self, chain: Chain, growth: float):
        self.db.collection("battery_actual").document("calculated").collection(
            str(chain.name)
        ).document(str(chain.collected)).set(
            {
                "growth": str(growth),
                "chain_started": str(chain.collected),
                "deprecated": False,
            }
        )
        self.remove_chain(chain)
        return self
