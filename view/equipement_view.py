from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit, 
                             QDialog, QComboBox, QSpinBox, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor
from model.database import Database
from datetime import datetime

class DialogAjouterEquipement(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Equipement")
        self.setGeometry(100, 100, 450, 350)
        self.db = Database()
        
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #ffffff, stop:1 #f5f5f5);
            }
            QLabel {
                font-weight: bold;
                color: #333333;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 2px solid #f79646;
                background-color: #fffaf6;
            }
            QPushButton {
                min-width: 100px;
                min-height: 35px;
            }
        """)
        
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        titre = QLabel("Nouvel Equipement")
        titre.setFont(QFont("Arial", 14, QFont.Bold))
        titre.setStyleSheet("color: #f79646;")
        layout.addRow(titre)
        
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Ex: Climatiseur Principal")
        self.type = QComboBox()
        self.type.addItems(["HVAC", "Eclairage", "Refroidissement", "Chauffage", "Electromenager", "Autre"])
        self.puissance = QSpinBox()
        self.puissance.setMaximum(50000)
        self.puissance.setSuffix(" W")
        self.puissance.setValue(1000)
        self.localisation = QLineEdit()
        self.localisation.setPlaceholderText("Ex: Salle Serveur")
        
        layout.addRow("Nom:", self.nom)
        layout.addRow("Type:", self.type)
        layout.addRow("Puissance:", self.puissance)
        layout.addRow("Localisation:", self.localisation)
        
        boutons = QHBoxLayout()
        boutons.setSpacing(10)
        btn_ok = QPushButton("Ajouter")
        btn_cancel = QPushButton("Annuler")
        btn_ok.setObjectName("success")
        btn_ok.setStyleSheet("""
            QPushButton#success {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #27ae60, stop:1 #229954);
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 25px;
                border: none;
            }
            QPushButton#success:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #2ecc71, stop:1 #1e8449);
            }
        """)
        
        btn_ok.clicked.connect(self.ajouter)
        btn_cancel.clicked.connect(self.reject)
        boutons.addWidget(btn_ok)
        boutons.addWidget(btn_cancel)
        
        layout.addRow(boutons)
        self.setLayout(layout)
    
    def ajouter(self):
        if not self.nom.text():
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        self.db.execute_insert(
            "INSERT INTO equipements(nom, type, puissance_w, localisation, statut, date_ajout) VALUES(?, ?, ?, ?, ?, ?)",
            (self.nom.text(), self.type.currentText(), self.puissance.value(), self.localisation.text(), "Inactif", datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        QMessageBox.information(self, "Succes", "Equipement ajoute avec succes!")
        self.accept()

class EquipementView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Titre
        titre = QLabel("GESTION DES EQUIPEMENTS")
        titre.setObjectName("title")
        titre.setFont(QFont("Arial", 22, QFont.Bold))
        titre.setStyleSheet("color: #f79646;")
        layout.addWidget(titre)

        # Statistiques equipements
        from PyQt5.QtWidgets import QGroupBox, QGridLayout
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(10)
        
        # Créer les widgets de statistiques
        self.stat_total = self.create_stat_box("Total Equipements", "0", "#3498db")
        self.stat_actifs = self.create_stat_box("Actifs", "0", "#27ae60")
        self.stat_inactifs = self.create_stat_box("Inactifs", "0", "#e74c3c")
        self.stat_puissance = self.create_stat_box("Puissance Totale", "0W", "#f79646")
        
        self.stats_layout.addWidget(self.stat_total)
        self.stats_layout.addWidget(self.stat_actifs)
        self.stats_layout.addWidget(self.stat_inactifs)
        self.stats_layout.addWidget(self.stat_puissance)
        
        layout.addLayout(self.stats_layout)

        # Boutons d'action avec animation
        boutons_layout = QHBoxLayout()
        boutons_layout.setSpacing(10)
        
        self.btn_ajouter = QPushButton("Ajouter Equipement")
        self.btn_modifier = QPushButton("Modifier")
        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_rafraichir = QPushButton("Rafraichir")
        
        # Style des boutons
        for btn in [self.btn_ajouter, self.btn_modifier, self.btn_rafraichir]:
            btn.setMinimumHeight(40)
        
        self.btn_supprimer.setObjectName("danger")
        self.btn_supprimer.setStyleSheet("""
            QPushButton#danger {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #e74c3c, stop:1 #c0392b);
            }
            QPushButton#danger:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ec7063, stop:1 #a93226);
            }
        """)
        
        self.btn_ajouter.clicked.connect(self.ajouter_equipement)
        self.btn_modifier.clicked.connect(self.modifier_equipement)
        self.btn_supprimer.clicked.connect(self.supprimer_equipement)
        self.btn_rafraichir.clicked.connect(self.charger_equipements)
        
        boutons_layout.addWidget(self.btn_ajouter)
        boutons_layout.addWidget(self.btn_modifier)
        boutons_layout.addWidget(self.btn_supprimer)
        boutons_layout.addWidget(self.btn_rafraichir)
        boutons_layout.addStretch()
        layout.addLayout(boutons_layout)

        # Tableau des équipements
        self.table_equipement = QTableWidget()
        self.table_equipement.setColumnCount(6)
        self.table_equipement.setHorizontalHeaderLabels([
            "ID", "Nom", "Type", "Puissance (W)", "Statut", "Localisation"
        ])
        self.table_equipement.setAlternatingRowColors(True)
        self.table_equipement.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_equipement.setSelectionMode(QTableWidget.SingleSelection)
        self.table_equipement.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        layout.addWidget(self.table_equipement)

        self.setLayout(layout)
        self.charger_equipements()
        self.mettre_a_jour_statistiques()
    
    def create_stat_box(self, label_text, value_text, color):
        """Créer une boîte de statistique"""
        from PyQt5.QtWidgets import QGroupBox
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
        stat_widget.value_label = value_label  # Stocker la référence du label
        return stat_widget
    
    def mettre_a_jour_statistiques(self):
        """Mettre à jour les statistiques des équipements"""
        equipements = self.db.execute_query("SELECT * FROM equipements")
        
        total = len(equipements)
        actifs = sum(1 for eq in equipements if eq[5] == "Actif")  # Colonne statut
        inactifs = total - actifs
        puissance_totale = sum(eq[3] for eq in equipements if eq[3] is not None)  # Colonne puissance_w
        
        # Mettre à jour les labels
        self.stat_total.value_label.setText(str(total))
        self.stat_actifs.value_label.setText(str(actifs))
        self.stat_inactifs.value_label.setText(str(inactifs))
        self.stat_puissance.value_label.setText(f"{puissance_totale:,}W")
    
    
    def charger_equipements(self):
        """Charger les équipements depuis la base de données"""
        self.table_equipement.setRowCount(0)
        equipements = self.db.execute_query("SELECT * FROM equipements")
        
        # Trier les équipements par puissance décroissante (colonne 3)
        equipements_tries = sorted(equipements, key=lambda x: x[3] if x[3] is not None else 0, reverse=True)
        
        for row, equipement in enumerate(equipements_tries):
            self.table_equipement.insertRow(row)
            for col, value in enumerate(equipement):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                # Colorer le statut
                if col == 4:
                    if "Actif" in str(value):
                        item.setForeground(QColor("#27ae60"))
                        item.setFont(QFont("Arial", 10, QFont.Bold))
                    else:
                        item.setForeground(QColor("#e74c3c"))
                        item.setFont(QFont("Arial", 10, QFont.Bold))
                self.table_equipement.setItem(row, col, item)
        
        self.table_equipement.resizeColumnsToContents()
    
    def ajouter_equipement(self):
        """Ajouter un nouvel équipement"""
        dialog = DialogAjouterEquipement(self)
        if dialog.exec_():
            self.charger_equipements()
            self.mettre_a_jour_statistiques()
    
    def modifier_equipement(self):
        """Modifier un équipement sélectionné"""
        row = self.table_equipement.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner un equipement")
            return
        
        equipement_id = self.table_equipement.item(row, 0).text()
        QMessageBox.information(self, "Info", "Fonction de modification en developpement")
    
    def supprimer_equipement(self):
        """Supprimer un équipement sélectionné"""
        row = self.table_equipement.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner un equipement")
            return
        
        equipement_id = self.table_equipement.item(row, 0).text()
        equipement_nom = self.table_equipement.item(row, 1).text()
        reply = QMessageBox.question(self, "Confirmation", f"Supprimer '{equipement_nom}' ?")
        
        if reply == QMessageBox.Yes:
            self.db.execute_delete("DELETE FROM equipements WHERE id = ?", (equipement_id,))
            QMessageBox.information(self, "Succes", "Equipement supprime avec succes")
            self.charger_equipements()
            self.mettre_a_jour_statistiques()

    def animate_entry(self):
        """Animation d'entrée"""
        pass
