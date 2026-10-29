from model.consommation_model import ConsommationModel

class ConsommationController:
    def __init__(self, db):
        self.model = ConsommationModel(db)
