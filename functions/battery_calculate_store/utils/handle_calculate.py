from typing import Type

from calculate.declination_calculate import CalculateDeclination
from calculate.growth_calculate import CalculateGrowth
from google.cloud import firestore
from models.chain import Chain
from models.chain_instance import ChainInstance


class HandleCalculate:
    def __init__(self):
        self.db = firestore.Client()

    @staticmethod
    def calculate_all(chain: Chain):
        growth = None
        declination = None

        prev_instance = None
        instance: Type[ChainInstance]

        for instance in chain.chain_instances:
            if prev_instance:

                if prev_instance.actual <= instance.actual:
                    growth = CalculateGrowth()
                    growth.add(instance, prev_instance)

                if prev_instance.actual > instance.actual:
                    declination = CalculateDeclination()
                    declination.add(instance, prev_instance)

            prev_instance = instance

        if growth:
            return growth.calculated(), declination.calculated()

    @staticmethod
    def should_store(chain: Chain):
        return len(chain.chain_instances) > 15 and chain.get_lowest().actual < 50

    def deprecate_chain(self, chain: Chain):
        chain = (
            self.db.collection("battery_actual")
            .document("chains")
            .collection(chain.name)
            .document(chain.collected)
        )
        chain.set({"deprecated": True})

    def remove_chain(self, chain: Chain):
        docs = (
            self.db.collection("battery_actual")
            .document("chains")
            .collection(chain.name)
            .document(chain.collected)
            .collection("collected")
            .stream()
        )

        for doc in docs:
            doc.reference.delete()

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

    def store_calculated(self, chain: Chain, *args):
        if self.should_store(chain) and not (args is None):
            self.db.collection("battery_actual").document("calculated").collection(
                str(chain.name)
            ).document(str(chain.collected)).set(
                {
                    "growth": str(args[0]),
                    "declination": str(args[1]),
                    "chain_started": str(chain.collected),
                    "deprecated": False,
                }
            )
            self.deprecate_chain(chain)
            return self

        self.remove_chain(chain)
        return self
