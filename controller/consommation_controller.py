class ConsommationController:
    def __init__(self, model):
        self.model = model

    def ajouter(self, equipement_id, source, duree, date):
        """Ajouter une consommation"""
        if duree <= 0:
            raise ValueError("Durée invalide")
        self.model.add(equipement_id, source, duree, date)
    
    def obtenir_consommation_totale(self):
        """Obtenir la consommation totale"""
        return self.model.get_total()
    
    def obtenir_consommation_par_equipement(self, equipement_id):
        """Obtenir la consommation d'un équipement"""
        return self.model.get_by_equipement(equipement_id)
    
    def obtenir_consommation_par_periode(self, date_debut, date_fin):
        """Obtenir la consommation sur une période"""
        return self.model.get_by_period(date_debut, date_fin)
