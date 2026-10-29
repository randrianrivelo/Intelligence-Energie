class SimulationController:
    def __init__(self):
        self.simulations = []
    
    def creer_simulation(self, nom, equipements, scenario):
        """Créer une nouvelle simulation"""
        simulation = {
            "nom": nom,
            "equipements": equipements,
            "scenario": scenario
        }
        self.simulations.append(simulation)
        return simulation
    
    def lancer_simulation(self, simulation_id):
        """Lancer une simulation"""
        print(f"Lancement simulation {simulation_id}")
    
    def arreter_simulation(self, simulation_id):
        """Arrêter une simulation"""
        print(f"Arrêt simulation {simulation_id}")
    
    def simuler_coupure(self):
        """Simuler une coupure JIRAMA"""
        print("Coupure JIRAMA → Groupe électrogène activé")
    
    def obtenir_resultats(self, simulation_id):
        """Obtenir les résultats d'une simulation"""
        return None
