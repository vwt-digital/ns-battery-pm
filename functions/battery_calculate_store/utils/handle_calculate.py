from typing import Type

from google.cloud import firestore
from models.chain import Chain
from models.chain_instance import ChainInstance


class HandleCalculate:
    def __init__(self):
        self.db = firestore.Client()

    @staticmethod
    def calculate_overall_growth(chain: Chain):
        diff_list = [float]

        prev_instance: Type[ChainInstance] = ChainInstance
        instance: Type[ChainInstance]

        for instance in chain.chain_instances:
            if prev_instance and prev_instance.actual <= instance.actual:
                diff_list.append(
                    (instance.actual - prev_instance.actual) / prev_instance.actual
                )
            prev_instance = instance

        return sum(diff_list) / len(diff_list)

    @staticmethod
    def calculate_fast_growth(chain: Chain):
        return NotImplemented

    @staticmethod
    def calculate_drip_growth(chain: Chain):
        return NotImplemented

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
            chain.add_chain_instance(ChainInstance.from_dict(instance.get().to_dict()))

        return chain.sort_chain_on_placed()

    def store_calculated(self, chain: Chain, growth: float):
        self.db.collection("battery_actual").document("calculated").collection(
            str(chain.name)
        ).document(str(chain.collected), {"growth": str(growth)})
        return self
