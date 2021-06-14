from calculate.calculate import Calculate
from models.chain_instance import ChainInstance


class CalculateGrowth(Calculate):
    def __init__(self):
        super().__init__()

    def add(self, instance: ChainInstance, prev_instance: ChainInstance):
        return super(CalculateGrowth, self).add(instance, prev_instance)

    def calculated(self):
        return super(CalculateGrowth, self).calculated()
