from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Titre principal
        titre = QLabel("TABLEAU DE BORD ENERGETIQUE")
        titre.setFont(QFont("Arial", 22, QFont.Bold))
        titre.setStyleSheet("color: #f79646;")
        layout.addWidget(titre)

        # ========== GRAPHIQUES ==========
        graphs_layout = QHBoxLayout()
        graphs_layout.setSpacing(15)
        
        # Graphique par equipement
        fig2 = Figure(figsize=(4, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        equipements = ['Clim', 'Eclairage', 'Refrig', 'Chauffage']
        valeurs = [250, 80, 150, 100]
        colors = ['#f79646', '#3498db', '#2ecc71', '#e74c3c']
        ax2.bar(equipements, valeurs, color=colors, edgecolor='#333', linewidth=1.5)
        ax2.set_title('Consommation par Equipement', fontweight='bold')
        ax2.set_ylabel('kWh')
        ax2.grid(True, alpha=0.3, axis='y')
        fig2.tight_layout()
        canvas2 = FigureCanvas(fig2)
        graphs_layout.addWidget(canvas2)
        
        # Graphique consommation horaire
        fig1 = Figure(figsize=(4, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        heures = ['00:00', '06:00', '12:00', '18:00', '23:00']
        consommation = [150, 250, 400, 600, 200]
        ax1.plot(heures, consommation, marker='o', color='#f79646', linewidth=2, markersize=8)
        ax1.fill_between(range(len(heures)), consommation, alpha=0.3, color='#f79646')
        ax1.set_title('Consommation par Heure', fontweight='bold')
        ax1.set_ylabel('kWh')
        ax1.grid(True, alpha=0.3)
        fig1.tight_layout()
        canvas1 = FigureCanvas(fig1)
        graphs_layout.addWidget(canvas1)
        
        layout.addLayout(graphs_layout)

        # ========== STATISTIQUES PRINCIPALES ==========
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        stats_data = [
            ("Consommation Aujourd'hui", "2,540 kWh", "#27ae60"),
            ("Pic Horaire", "850 kWh/h", "#e74c3c"),
            ("Moyenne Mensuelle", "2,300 kWh", "#3498db"),
            ("Economie Estimee", "120 kWh", "#2ecc71")
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
            stat_layout = QVBoxLayout()
            value_label = QLabel(value_text)
            value_label.setFont(QFont("Arial", 16, QFont.Bold))
            value_label.setStyleSheet(f"color: {color};")
            stat_layout.addWidget(value_label)
            stat_widget.setLayout(stat_layout)
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)

        # ========== TABLEAU DETAILLE ==========
        label_tableau = QLabel("Consommation Detaillee")
        label_tableau.setFont(QFont("Arial", 14, QFont.Bold))
        label_tableau.setStyleSheet("color: #f79646; margin-top: 10px;")
        layout.addWidget(label_tableau)

        self.table_consommation = QTableWidget()
        self.table_consommation.setColumnCount(6)
        self.table_consommation.setHorizontalHeaderLabels([
            "Equipement", "Consommation (kWh)", "Statut", "Dernier Releve", "Puissance (W)", "Localisation"
        ])
        self.table_consommation.setRowCount(6)
        self.table_consommation.setAlternatingRowColors(True)
        self.table_consommation.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        
        # Donnees d'exemple
        data = [
            ["Climatisation Principale", "250", "Actif", "14:30", "3500W", "Salle Serveur"],
            ["Eclairage Salle Reunion", "80", "Actif", "14:30", "400W", "Salle Reunion"],
            ["Refrigeration Cuisine", "150", "Actif", "14:30", "800W", "Cuisine"],
            ["Chauffage Couloirs", "0", "Inactif", "14:30", "5000W", "Couloir"],
            ["Projecteurs LED", "35", "Actif", "14:30", "200W", "Bureau"],
            ["Autres Equipements", "85", "Actif", "14:30", "1200W", "Divers"]
        ]
        
        for row, item_data in enumerate(data):
            for col, value in enumerate(item_data):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                # Colorer le statut
                if col == 2:
                    if "Actif" in value:
                        item.setForeground(QColor("#27ae60"))
                        item.setFont(QFont("Arial", 10, QFont.Bold))
                    else:
                        item.setForeground(QColor("#e74c3c"))
                        item.setFont(QFont("Arial", 10, QFont.Bold))
                
                self.table_consommation.setItem(row, col, item)

        self.table_consommation.resizeColumnsToContents()
        layout.addWidget(self.table_consommation)

        # ========== INFORMATIONS IMPORTANTES ==========
        info_layout = QGridLayout()
        info_layout.setSpacing(10)
        
        info_items = [
            ("Source Active", "JIRAMA - Reseau Principal"),
            ("Dernier Releve", "2025-01-15 14:35:00"),
            ("Etat Systeme", "Normal - Operationnel"),
            ("Efficacite Energetique", "85% - Bon"),
        ]
        
        for idx, (title, value) in enumerate(info_items):
            title_label = QLabel(title + ":")
            title_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_label = QLabel(value)
            value_label.setFont(QFont("Arial", 10))
            value_label.setStyleSheet("color: #f79646;")
            
            info_layout.addWidget(title_label, idx // 2, (idx % 2) * 2)
            info_layout.addWidget(value_label, idx // 2, (idx % 2) * 2 + 1)
        
        layout.addLayout(info_layout)
        layout.addStretch()

        self.setLayout(layout)

    def animate_entry(self):
        """Animation d'entree du tableau de bord"""
        pass
