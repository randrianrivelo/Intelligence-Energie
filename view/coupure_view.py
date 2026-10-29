from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor
from model.database import Database

class CoupureView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Titre
        titre = QLabel("HISTORIQUE DES COUPURES D'ENERGIE")
        titre.setObjectName("title")
        titre.setFont(QFont("Arial", 22, QFont.Bold))
        titre.setStyleSheet("color: #f79646;")
        layout.addWidget(titre)

        # Statistiques des coupures
        from PyQt5.QtWidgets import QGroupBox, QGridLayout
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        
        stats_data = [
            ("Coupures ce Mois", "2", "#e74c3c"),
            ("Temps Total", "45 min", "#3498db"),
            ("Duree Moyenne", "22 min", "#f79646"),
            ("Derniere Coupure", "2025-01-10", "#2ecc71"),
        ]
        
        for label_text, value_text, color in stats_data:
            stat_widget = QGroupBox(label_text)
            stat_widget.setStyleSheet(f"""
                QGroupBox {{
                    color: #333333;
                    font-weight: bold;
                    border: 2px solid {color};
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }}
            """)
            stat_lay = QVBoxLayout()
            value_label = QLabel(value_text)
            value_label.setFont(QFont("Arial", 14, QFont.Bold))
            value_label.setStyleSheet(f"color: {color};")
            stat_lay.addWidget(value_label)
            stat_widget.setLayout(stat_lay)
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)

        # Boutons d'action
        boutons_layout = QHBoxLayout()
        boutons_layout.setSpacing(10)
        
        self.btn_voir_historique = QPushButton("Voir Historique")
        self.btn_simuler_coupure = QPushButton("Simuler une Coupure")
        self.btn_actualiser_coupures = QPushButton("Actualiser")
        
        for btn in [self.btn_voir_historique, self.btn_simuler_coupure, self.btn_actualiser_coupures]:
            btn.setMinimumHeight(40)
        
        self.btn_simuler_coupure.setObjectName("danger")
        self.btn_simuler_coupure.setStyleSheet("""
            QPushButton#danger {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton#danger:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ec7063, stop:1 #a93226);
            }
        """)
        
        self.btn_voir_historique.clicked.connect(self.voir_historique_coupures)
        self.btn_simuler_coupure.clicked.connect(self.simuler_coupure)
        self.btn_actualiser_coupures.clicked.connect(self.charger_coupures)
        
        boutons_layout.addWidget(self.btn_voir_historique)
        boutons_layout.addWidget(self.btn_simuler_coupure)
        boutons_layout.addWidget(self.btn_actualiser_coupures)
        boutons_layout.addStretch()
        layout.addLayout(boutons_layout)

        # Tableau des coupures
        self.table_coupures = QTableWidget()
        self.table_coupures.setColumnCount(5)
        self.table_coupures.setHorizontalHeaderLabels([
            "ID", "Equipement", "Debut", "Fin", "Duree"
        ])
        self.table_coupures.setAlternatingRowColors(True)
        self.table_coupures.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_coupures.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        layout.addWidget(self.table_coupures)

        self.setLayout(layout)
        self.charger_coupures()
    
    def charger_coupures(self):
        """Charger les coupures depuis la base de donnees"""
        self.table_coupures.setRowCount(0)
        coupures = self.db.execute_query("SELECT * FROM coupures")
        
        if not coupures:
            # Donnees d'exemple
            data_coupures = [
                ("Refrigerateur", "2025-01-15 13:45", "2025-01-15 14:05", "20 min"),
                ("Eclairage Couloir", "2025-01-14 22:30", "2025-01-14 22:45", "15 min"),
                ("Projecteurs Salle 3", "2025-01-13 10:15", "2025-01-13 10:30", "15 min")
            ]
            for row, coupure_data in enumerate(data_coupures):
                self.table_coupures.insertRow(row)
                for col, value in enumerate(coupure_data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
                    # Colorier les durées longues
                    if col == 4:
                        if "20" in value or "30" in value:
                            item.setForeground(QColor("#e74c3c"))
                            item.setFont(QFont("Arial", 10, QFont.Bold))
                        else:
                            item.setForeground(QColor("#f39c12"))
                    
                    self.table_coupures.setItem(row, col, item)
        else:
            for row, coupure in enumerate(coupures):
                self.table_coupures.insertRow(row)
                for col, value in enumerate(coupure):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_coupures.setItem(row, col, item)
        
        self.table_coupures.resizeColumnsToContents()
    
    def voir_historique_coupures(self):
        """Voir l'historique des coupures avec statistiques réelles"""
        from datetime import datetime, timedelta
        
        # Récupérer toutes les coupures
        coupures = self.db.execute_query("SELECT * FROM coupures")
        
        if not coupures:
            QMessageBox.information(self, "Historique des Coupures", 
            """
            === Historique des coupures ===
            
            Aucune coupure enregistrée.
            """)
            return
        
        # Calculer les statistiques
        total_coupures = len(coupures)
        duree_totale = sum(c[4] for c in coupures if c[4] is not None)  # durée_minutes
        duree_moyenne = duree_totale // total_coupures if total_coupures > 0 else 0
        
        # Trouver la dernière coupure
        dates_fin = [c[3] for c in coupures if c[3] is not None]
        derniere_coupure = max(dates_fin) if dates_fin else "N/A"
        
        # Récupérer les noms des équipements pour la dernière coupure
        dernier_equipement = "N/A"
        for coupure in coupures:
            if coupure[3] == derniere_coupure:
                equipement = self.db.execute_query(f"SELECT nom FROM equipements WHERE id = {coupure[1]}")
                if equipement:
                    dernier_equipement = equipement[0][0]
                break
        
        # Compter les coupures du mois actuel
        maintenant = datetime.now()
        debut_mois = maintenant.replace(day=1)
        coupures_ce_mois = sum(1 for c in coupures if c[2] is not None and 
                                datetime.fromisoformat(c[2].replace('Z', '+00:00')) >= debut_mois)
        
        # Afficher les statistiques
        message = f"""
=== HISTORIQUE DES COUPURES ===

Statistiques Générales:
  • Coupures enregistrées: {total_coupures}
  • Coupures ce mois: {coupures_ce_mois}
  • Durée totale: {duree_totale} minutes ({duree_totale // 60}h {duree_totale % 60}min)
  • Durée moyenne: {duree_moyenne} minutes

Dernière Coupure:
  • Date/Heure: {derniere_coupure}
  • Équipement: {dernier_equipement}

Analyse:
  • Fréquence: {total_coupures} incidents au total
  • Impacte: Impact sur {total_coupures} équipement(s) différent(s)
        """
        
        QMessageBox.information(self, "Historique des Coupures", message)
    
    def signaler_coupure(self):
        """Signaler une nouvelle coupure"""
        QMessageBox.information(self, "Signalement", "Fonction de signalement de coupure en developpement")

    def animate_entry(self):
        """Animation d'entrée"""
        pass
    
    def charger_coupures(self):
        """Charger les coupures depuis la base de donnees"""
        self.table_coupures.setRowCount(0)
        coupures = self.db.execute_query("SELECT * FROM coupures")
        
        if not coupures:
            # Donnees d'exemple
            data_coupures = [
                ("Refrigerateur", "2025-01-15 13:45", "2025-01-15 14:05", "20 min"),
                ("Eclairage Couloir", "2025-01-14 22:30", "2025-01-14 22:45", "15 min"),
                ("Projecteurs Salle 3", "2025-01-13 10:15", "2025-01-13 10:30", "15 min")
            ]
            for row, coupure_data in enumerate(data_coupures):
                self.table_coupures.insertRow(row)
                for col, value in enumerate(coupure_data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_coupures.setItem(row, col, item)
        else:
            for row, coupure in enumerate(coupures):
                self.table_coupures.insertRow(row)
                for col, value in enumerate(coupure):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_coupures.setItem(row, col, item)
        
        self.table_coupures.resizeColumnsToContents()
    
    def voir_historique_coupures(self):
        """Voir l'historique des coupures"""
        QMessageBox.information(self, "Historique", "Affichage de l'historique des coupures")
    
    def signaler_coupure(self):
        """Signaler une nouvelle coupure"""
        QMessageBox.information(self, "Info", "Fonction de signalement de coupure en developpement")

    def simuler_coupure(self):
        """Simuler une coupure basée sur les conditions"""
        import random
        from datetime import datetime, timedelta
        
        # Liste des équipements
        equipements = self.db.execute_query("SELECT id, nom, puissance_w FROM equipements")
        if not equipements:
            QMessageBox.warning(self, "Erreur", "Aucun équipement disponible pour la simulation")
            return
        
        # Sélectionner un équipement aléatoire
        equipement = random.choice(equipements)
        equipement_id = equipement[0]
        equipement_nom = equipement[1]
        puissance = equipement[2] if equipement[2] else 0
        
        # Raisons possibles de coupure avec probabilités basées sur les conditions
        raisons = [
            {
                "condition": puissance > 3000,
                "raison": "Surcharge électrique",
                "probabilite": 0.4
            },
            {
                "raison": "Maintenance programmée",
                "probabilite": 0.25
            },
            {
                "raison": "Surtension détectée",
                "probabilite": 0.2
            },
            {
                "raison": "Défaut circuit",
                "probabilite": 0.1
            },
            {
                "raison": "Problème réseau JIRAMA",
                "probabilite": 0.05
            }
        ]
        
        # Sélectionner une raison basée sur les conditions
        raison_selectionnee = None
        
        # Vérifier d'abord les conditions spéciales
        for r in raisons:
            if "condition" in r and r["condition"]:
                if random.random() < r["probabilite"]:
                    raison_selectionnee = r["raison"]
                    break
        
        # Sinon, sélectionner aléatoirement
        if not raison_selectionnee:
            raison_selectionnee = random.choices(
                [r["raison"] for r in raisons],
                weights=[r["probabilite"] for r in raisons],
                k=1
            )[0]
        
        # Générer une durée aléatoire (5 à 120 minutes)
        duree_minutes = random.randint(5, 120)
        
        # Créer les timestamps
        date_debut = datetime.now()
        date_fin = date_debut + timedelta(minutes=duree_minutes)
        
        # Insérer la coupure dans la base de données
        try:
            self.db.execute_insert(
                "INSERT INTO coupures(equipement_id, date_debut, date_fin, durée_minutes, raison) VALUES(?, ?, ?, ?, ?)",
                (
                    equipement_id,
                    date_debut.strftime("%Y-%m-%d %H:%M:%S"),
                    date_fin.strftime("%Y-%m-%d %H:%M:%S"),
                    duree_minutes,
                    raison_selectionnee
                )
            )
            QMessageBox.information(
                self, 
                "Coupure Simulée", 
                f"Coupure enregistrée:\n\n"
                f"Équipement: {equipement_nom}\n"
                f"Raison: {raison_selectionnee}\n"
                f"Début: {date_debut.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Fin: {date_fin.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Durée: {duree_minutes} minutes"
            )
            self.charger_coupures()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création de la coupure: {str(e)}")
