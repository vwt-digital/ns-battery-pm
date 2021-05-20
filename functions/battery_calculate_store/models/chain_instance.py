from typing import Any


class ChainInstance(object):
    def __init__(self, actual: float, placed: Any):
        self.actual = actual
        self.placed = placed

    @staticmethod
    def from_dict(source):
        return ChainInstance(
            source["actual"],
            source["collected"],
        )
