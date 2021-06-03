from datetime import datetime
from typing import Any, List

from models.chain_instance import ChainInstance


class Chain(object):
    def __init__(self, collected: Any, name: str):
        self.collected = collected
        self.name = name
        self.chain_instances = []

    @staticmethod
    def from_dict(source):
        return Chain(source["collected"], source["name"])

    @staticmethod
    def __sort(chain_instances: List[ChainInstance]):
        return sorted(
            chain_instances,
            key=lambda x: datetime.strptime(x.placed, "%Y-%m-%dT%H:%M:%SZ"),
        )

    def get_lowest(self):
        return min(self.chain_instances, key=lambda x: x.actual)

    def sort_chain_on_placed(self):
        self.chain_instances = self.__sort(self.chain_instances)
        return self

    def add_chain_instance(self, chain_instance: ChainInstance):
        self.chain_instances.append(chain_instance)
        return self
