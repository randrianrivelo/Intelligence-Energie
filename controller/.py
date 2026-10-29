class SimulationController:
    def __init__(self):
        self.jirama = True

    def couper(self):
        self.jirama = False
        return "Coupure JIRAMA - groupe électrogène activé"

    def retablir(self):
        self.jirama = True
        return "JIRAMA rétablie"
