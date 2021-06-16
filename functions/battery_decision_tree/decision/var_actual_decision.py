from decision.decision import Decision


class VarActualDecision(Decision):
    def __init__(self, battery: str):
        super(VarActualDecision, self).__init__(battery)

    def __decide(self, a: float, b: float, limit: float = 0.001):
        """
        Decide battery absolute downfall by setting a maximum growth rate and minimum decline rate,
        and look for the point when y intercepts those points.

        y = ax + b
        y being the level at any point of x (weeks), calculated by a (growth / decline rate) + b (initial)
        """
        # if (
        #         last_stored - (average_growth_change_rate * limit)
        #         > self.deciding_growth_limit
        # ):
        # return Advice.SAFE.value.format(weeks=limit)
        #
        # for x in range(limit):
        #     if (
        #             last_stored - (average_growth_change_rate * (x + 1))
        #             <= self.deciding_growth_limit
        #     ):
        #         return Decision.UNSAFE.value.format(weeks=x + 1)
        # return Decision.UNDETERMINED.value

    def generate_decision(self):
        pass
