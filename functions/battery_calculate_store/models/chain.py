from typing import Any, List

from models.chain_instance import ChainInstance


class Chain(object):
    def __init__(self, collected: Any, chains: List[ChainInstance]):
        self.collected = collected
        self.chains = chains

    @staticmethod
    def from_dict(source) -> object:
        return Chain(source["collected"], source["chains"])

    def add_chain_instance(self, chain_instance: ChainInstance) -> object:
        self.chains.append(chain_instance)
        return self
