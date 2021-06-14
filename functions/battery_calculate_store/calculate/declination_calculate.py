from calculate.calculate import Calculate
from models.chain_instance import ChainInstance


class CalculateDeclination(Calculate):
    def __init__(self):
        super().__init__()

    def add(self, instance: ChainInstance, prev_instance: ChainInstance):
        return super(CalculateDeclination, self).add(instance, prev_instance)

    def calculated(self):
        return super(CalculateDeclination, self).calculated()
