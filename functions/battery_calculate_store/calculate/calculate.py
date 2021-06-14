from datetime import datetime

from models.chain_instance import ChainInstance


class Calculate:
    def __init__(self):
        self.tmp_calculated = []

    def add(self, instance: ChainInstance, prev_instance: ChainInstance):
        between_dates_s = (
            datetime.strptime(instance.placed, "%Y-%m-%dT%H:%M:%SZ")
            - datetime.strptime(prev_instance.placed, "%Y-%m-%dT%H:%M:%SZ")
        ).total_seconds()
        r_difference = (instance.actual - prev_instance.actual) / prev_instance.actual
        self.tmp_calculated.append((r_difference / between_dates_s) * 60)
        return self

    def calculated(self) -> float:
        return float(sum(self.tmp_calculated)) / float(len(self.tmp_calculated))
