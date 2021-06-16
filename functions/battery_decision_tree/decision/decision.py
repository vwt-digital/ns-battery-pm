from models.enum import Advice


class Decision:
    def __init__(self, battery: str):
        self.battery = battery

    def decide(self, a: float, b: float, limit: float):
        """
        Decide battery absolute downfall by setting a maximum growth rate and minimum decline rate,
        and look for the point when y intercepts those points.

        y = ax + b
        y being the level at any point of x (weeks), calculated by a (growth / decline rate) + b (initial)
        """
        try:
            return Advice.DETERMINED.value.format(weeks=(limit - b) / a)
        except Exception as e:
            print(self.battery, e)
            return Advice.UNDETERMINED

    def generate_decision(self, *args, **kwargs):
        return ""
