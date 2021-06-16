from decision.decision import Decision


class VarActualDecision(Decision):
    def __init__(self, battery: str):
        super(VarActualDecision, self).__init__(battery)

    def generate_decision(self, calc, current, limit=1e-3, *args, **kwargs):
        return self.decide(a=calc, b=current, limit=limit)
