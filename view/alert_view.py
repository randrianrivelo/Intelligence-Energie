from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor
from model.database import Database

class AlertView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Titre
        titre = QLabel("GESTION DES ALERTES SYSTEME")
        titre.setObjectName("title")
        titre.setFont(QFont("Arial", 22, QFont.Bold))
        titre.setStyleSheet("color: #f79646;")
        layout.addWidget(titre)

        # Statistiques d'alertes
        from PyQt5.QtWidgets import QGroupBox, QGridLayout
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        
        stats_data = [
            ("Alertes Actives", "3", "#e74c3c"),
            ("Alertes Resolues", "12", "#27ae60"),
            ("En Attente", "2", "#f79646"),
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
        
        self.btn_resoudre = QPushButton("Marquer comme Resolu")
        self.btn_details_alerte = QPushButton("Voir Details")
        self.btn_actualiser_alertes = QPushButton("Actualiser")
        self.btn_simuler = QPushButton("Simuler une Alerte")
        
        for btn in [self.btn_resoudre, self.btn_details_alerte, self.btn_actualiser_alertes, self.btn_simuler]:
            btn.setMinimumHeight(40)
        
        self.btn_resoudre.setObjectName("success")
        self.btn_simuler.setObjectName("warning")
        self.btn_simuler.setStyleSheet("""
            QPushButton#warning {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #f39c12, stop:1 #d68910);
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton#warning:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #f8b739, stop:1 #e67e22);
            }
        """)
        self.btn_resoudre.setStyleSheet("""
            QPushButton#success {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #27ae60, stop:1 #229954);
            }
            QPushButton#success:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #2ecc71, stop:1 #1e8449);
            }
        """)
        
        self.btn_resoudre.clicked.connect(self.resoudre_alerte)
        self.btn_details_alerte.clicked.connect(self.voir_details_alerte)
        self.btn_actualiser_alertes.clicked.connect(self.charger_alertes)
        self.btn_simuler.clicked.connect(self.simuler_alerte)
        
        boutons_layout.addWidget(self.btn_resoudre)
        boutons_layout.addWidget(self.btn_details_alerte)
        boutons_layout.addWidget(self.btn_actualiser_alertes)
        boutons_layout.addWidget(self.btn_simuler)
        boutons_layout.addStretch()
        layout.addLayout(boutons_layout)

        # Tableau des alertes
        self.table_alertes = QTableWidget()
        self.table_alertes.setColumnCount(5)
        self.table_alertes.setHorizontalHeaderLabels([
            "ID", "Type", "Equipement", "Message", "Date/Heure"
        ])
        self.table_alertes.setAlternatingRowColors(True)
        self.table_alertes.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_alertes.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        layout.addWidget(self.table_alertes)

        self.setLayout(layout)
        self.charger_alertes()
    
    def charger_alertes(self):
        """Charger les alertes depuis la base de donnees"""
        self.table_alertes.setRowCount(0)
        alertes = self.db.execute_query("SELECT * FROM alertes WHERE statut = 'Active'")
        
        if not alertes:
            # Donnees d'exemple
            data_alertes = [
                ("Consommation Elevee", "Climatiseur Principal", "Consommation > 3000W", "2025-01-15 14:35"),
                ("Coupure", "Refrigerateur", "Equipement hors ligne", "2025-01-15 13:45"),
                ("Temperature", "Salle Serveur", "Temperature > 25C", "2025-01-15 14:20"),
                ("Maintenance", "Climatiseur Auxiliaire", "Maintenance requise", "2025-01-15 12:00")
            ]
            for row, alerte_data in enumerate(data_alertes):
                self.table_alertes.insertRow(row)
                for col, value in enumerate(alerte_data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
                    # Colorer les types d'alertes
                    if col == 1:
                        if "Consommation" in value:
                            item.setForeground(QColor("#f39c12"))
                            item.setFont(QFont("Arial", 10, QFont.Bold))
                        elif "Coupure" in value:
                            item.setForeground(QColor("#e74c3c"))
                            item.setFont(QFont("Arial", 10, QFont.Bold))
                        elif "Temperature" in value:
                            item.setForeground(QColor("#e67e22"))
                            item.setFont(QFont("Arial", 10, QFont.Bold))
                    
                    self.table_alertes.setItem(row, col, item)
        else:
            for row, alerte in enumerate(alertes):
                self.table_alertes.insertRow(row)
                for col, value in enumerate(alerte):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_alertes.setItem(row, col, item)
        
        self.table_alertes.resizeColumnsToContents()
    
    def resoudre_alerte(self):
        """Marquer une alerte comme resolue"""
        row = self.table_alertes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner une alerte")
            return
        
        alerte_id = self.table_alertes.item(row, 0).text()
        self.db.execute_update("UPDATE alertes SET statut = ? WHERE id = ?", ("Resolue", alerte_id))
        QMessageBox.information(self, "Succes", "Alerte marquee comme resolue")
        self.charger_alertes()
    
    def voir_details_alerte(self):
        """Voir les details d'une alerte"""
        row = self.table_alertes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner une alerte")
            return
        
        alerte_id = self.table_alertes.item(row, 0).text()
        alerte_type = self.table_alertes.item(row, 1).text()
        equipement = self.table_alertes.item(row, 2).text()
        message = self.table_alertes.item(row, 3).text()
        date = self.table_alertes.item(row, 4).text()
        
        details = f"""
        === Details de l'Alerte ===
        
        ID: {alerte_id}
        Type: {alerte_type}
        Equipement: {equipement}
        Message: {message}
        Date/Heure: {date}
        """
        QMessageBox.information(self, "Details de l'Alerte", details)

    def animate_entry(self):
        """Animation d'entree du tableau d'alertes"""
        pass
    
    def simuler_alerte(self):
        """Simuler une alerte basée sur les conditions"""
        import random
        from datetime import datetime
        
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
        
        # Conditions et types d'alertes
        conditions = [
            {
                "condition": puissance > 3000,
                "type": "Consommation Elevee",
                "message": f"La puissance dépasse 3000W ({puissance}W)"
            },
            {
                "condition": random.random() < 0.3,
                "type": "Temperature",
                "message": "Température détectée > 25°C"
            },
            {
                "condition": random.random() < 0.2,
                "type": "Coupure",
                "message": "Équipement hors ligne - Perte de signal"
            },
            {
                "condition": random.random() < 0.25,
                "type": "Maintenance",
                "message": "Maintenance programmée requise"
            },
            {
                "condition": random.random() < 0.15,
                "type": "Anomalie",
                "message": "Fluctuation anormale de courant détectée"
            }
        ]
        
        # Appliquer les conditions
        alertes_possibles = [c for c in conditions if c["condition"]]
        
        if not alertes_possibles:
            # Si aucune condition n'est remplie, générer une alerte aléatoire
            alerte = random.choice(conditions[:2])
        else:
            alerte = random.choice(alertes_possibles)
        
        # Insérer l'alerte dans la base de données
        try:
            date_alerte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.execute_insert(
                "INSERT INTO alertes(type, equipement_id, message, date_creation, statut) VALUES(?, ?, ?, ?, ?)",
                (alerte["type"], equipement_id, alerte["message"], date_alerte, "Active")
            )
            QMessageBox.information(
                self, 
                "Alerte Simulée", 
                f"Alerte créée:\n\n"
                f"Type: {alerte['type']}\n"
                f"Équipement: {equipement_nom}\n"
                f"Message: {alerte['message']}\n"
                f"Date: {date_alerte}"
            )
            self.charger_alertes()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création de l'alerte: {str(e)}")
    
    def charger_alertes(self):
        """Charger les alertes depuis la base de donnees"""
        self.table_alertes.setRowCount(0)
        alertes = self.db.execute_query("SELECT * FROM alertes WHERE statut = 'Active'")
        
        if not alertes:
            # Donnees d'exemple
            data_alertes = [
                ("1", "Consommation Elevee", "Climatiseur Principal", "Consommation > 3000W", "2025-01-15 14:35"),
                ("2", "Coupure", "Refrigerateur", "Equipement hors ligne", "2025-01-15 13:45"),
                ("3", "Temperature", "Salle Serveur", "Temperature > 25C", "2025-01-15 14:20"),
            ]
            for row, alerte_data in enumerate(data_alertes):
                self.table_alertes.insertRow(row)
                for col, value in enumerate(alerte_data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_alertes.setItem(row, col, item)
        else:
            for row, alerte in enumerate(alertes):
                self.table_alertes.insertRow(row)
                for col, value in enumerate(alerte):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_alertes.setItem(row, col, item)
        
        self.table_alertes.resizeColumnsToContents()
    
    def resoudre_alerte(self):
        """Marquer une alerte comme resolue"""
        row = self.table_alertes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner une alerte")
            return
        
        alerte_id = self.table_alertes.item(row, 0).text()
        self.db.execute_update("UPDATE alertes SET statut = ? WHERE id = ?", ("Resolue", alerte_id))
        QMessageBox.information(self, "Succes", "Alerte marquee comme resolue")
        self.charger_alertes()
