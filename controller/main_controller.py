from model.database import Database
from datetime import datetime

class MainController:
    def __init__(self, view):
        self.view = view
        self.db = Database()
        self.setup_connections()
        self.initialiser_donnees_exemple()
    
    def setup_connections(self):
        """Connecter les signaux des boutons aux fonctions"""
        try:
            # Connexions pour la page Équipements
            equipement_view = self.view.tabs.widget(1)
            if hasattr(equipement_view, 'btn_ajouter'):
                equipement_view.btn_ajouter.clicked.connect(equipement_view.ajouter_equipement)
        except Exception as e:
            print(f"Erreur setup_connections: {e}")
    
    def initialiser_donnees_exemple(self):
        """Initialiser avec des données d'exemple"""
        # Vérifier si des équipements existent déjà
        equipements = self.db.execute_query("SELECT COUNT(*) as count FROM equipements")
        
        if equipements and equipements[0][0] == 0:
            # Ajouter des équipements d'exemple
            data_exemple = [
                ("Climatiseur Principal", "HVAC", 3500, "Salle Serveur", "Actif"),
                ("Climatiseur Auxiliaire", "HVAC", 2500, "Bureau", "Actif"),
                ("Projecteurs LED", "Eclairage", 400, "Salle Reunion", "Actif"),
                ("Refrigerateur", "Refroidissement", 800, "Cuisine", "Actif"),
                ("Chauffage", "HVAC", 5000, "Couloir", "Inactif"),
                ("Distributeur", "Electromenager", 200, "Accueil", "Actif")
            ]
            
            for nom, type_eq, puissance, localisation, statut in data_exemple:
                self.db.execute_insert(
                    "INSERT INTO equipements(nom, type, puissance_w, localisation, statut, date_ajout) VALUES(?, ?, ?, ?, ?, ?)",
                    (nom, type_eq, puissance, localisation, statut, datetime.now().strftime("%Y-%m-%d %H:%M"))
                )
    
    def charger_donnees(self):
        """Charger les données de la base de données"""
        try:
            equipements = self.db.execute_query("SELECT COUNT(*) FROM equipements")
            alertes = self.db.execute_query("SELECT COUNT(*) FROM alertes")
            coupures = self.db.execute_query("SELECT COUNT(*) FROM coupures")
            print(f"Donnees chargees: {equipements}, {alertes}, {coupures}")
        except Exception as e:
            print(f"Erreur charger_donnees: {e}")
