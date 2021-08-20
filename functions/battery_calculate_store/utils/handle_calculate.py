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
        """
        :param chain:
        :return:
        """
        growth = CalculateGrowth()
        declination = CalculateDeclination()

        prev_instance = None

        for instance in chain.chain_instances:
            if prev_instance:

                if prev_instance.actual <= instance.actual:
                    # Delta is positive relative to the previous instance's actual
                    growth.add(instance, prev_instance)

                if prev_instance.actual > instance.actual:
                    # Delta is negative relative to the previous instance's actual
                    declination.add(instance, prev_instance)

            prev_instance = instance

        return growth.calculated(), declination.calculated()

    @staticmethod
    def should_store(chain: Chain):
        """
            If the length of the chain instances is lower than 12, or when the lowest chain instance's actual is higher than 49,
            it will not store. The amount of data will be insufficient to create a valid prediction.
        :param chain:
        :return:
        """

        return len(chain.chain_instances) >= 12 and chain.get_lowest().actual < 50

    def deprecate_chain(self, chain: Chain):
        """
        :param chain:
        """
        chain = (
            self.db.collection("battery_actual")
            .document("chains").collection(chain.name).document(chain.collected)
        )
        chain.set({"deprecated": True})

    def remove_chain(self, chain: Chain):
        """
        :param chain:
        """
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
        """
        :param chain_name:
        :return:
        """
        battery_collection = (
            self.db.collection("battery_actual")
                .document("chains")
                .collection(str(chain_name))
        )
        r_chain = battery_collection.document(
            [
                x.id
                for x in battery_collection.order_by(
                    "chain_started", direction=firestore.Query.DESCENDING)
                .limit(1).stream()
            ][0]
        )
        chain = Chain.from_dict({"collected": r_chain.id, "name": chain_name})

        for instance in r_chain.collection("collected").stream():
            chain.add_chain_instance(ChainInstance.from_dict(instance.to_dict()))

        return chain.sort_chain_on_placed()

    def store_calculated(self, chain: Chain, growth, declination):
        """
        :param chain:
        :param growth:
        :param declination:
        :return: HandleCalculate
        """
        self.db.collection("battery_actual").document("calculated").collection(
            str(chain.name)
        ).document(str(chain.collected)).set(
            {
                "growth": str(growth),
                "declination": str(declination),
                "chain_started": str(chain.collected),
                "deprecated": False,
            }
        )
        self.deprecate_chain(chain)
        return self
