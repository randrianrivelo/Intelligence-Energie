from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from view.dashboard_view import DashboardView
from view.equipement_view import EquipementView
from view.alert_view import AlertView
from view.coupure_view import CoupureView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JIRAMA - Gestion Energetique")
        self.setGeometry(100, 100, 1400, 800)

        # Style moderne avec dégradés et ombres
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabBar {
                background-color: transparent;
                border-bottom: 3px solid #f79646;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ffffff, stop:1 #f0f0f0);
                color: #555555;
                padding: 15px 35px;
                border: 2px solid #e0e0e0;
                border-bottom: none;
                margin-right: 3px;
                font-weight: 600;
                font-size: 13px;
                font-style: normal;
                border-radius: 8px 8px 0px 0px;
                min-width: 120px;
                text-align: center;
            }
            QTabBar::tab:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #fff5f0, stop:1 #ffe8dc);
                border: 2px solid #f79646;
                color: #f79646;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ff9966, stop:1 #f79646);
                color: white;
                border: 2px solid #f79646;
                font-weight: bold;
                font-style: normal;
            }
            QTabWidget::pane {
                border: 3px solid #f79646;
                border-top: none;
                background-color: white;
                border-radius: 0px 0px 8px 8px;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: #f79646;
                padding: 10px;
            }
            QLabel#info {
                font-size: 13px;
                color: #666666;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ff9966, stop:1 #f79646);
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 12px 24px;
                border: none;
                font-size: 12px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ff8040, stop:1 #e06e1f);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #d45e0f, stop:1 #c24f0f);
                padding: 14px 24px 10px 24px;
            }
            QPushButton#danger {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #e74c3c, stop:1 #c0392b);
            }
            QPushButton#danger:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ec7063, stop:1 #a93226);
            }
            QPushButton#success {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #27ae60, stop:1 #229954);
            }
            QPushButton#success:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #2ecc71, stop:1 #1e8449);
            }
            QTableWidget {
                background-color: white;
                gridline-color: #e0e0e0;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                selection-background-color: #ffe8dc;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #ffe8dc;
                color: #333333;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ff9966, stop:1 #f79646);
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 2px solid #f79646;
                background-color: #fffaf6;
            }
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #ffffff, stop:1 #f5f5f5);
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ffb399, stop:1 #f79646);
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #ff9966, stop:1 #f27d3f);
            }
        """)

        # Créer les onglets avec animations
        self.tabs = QTabWidget()
        self.tabs.setMovable(False)
        self.tabs.setTabPosition(QTabWidget.North)
        
        self.dashboard = DashboardView()
        self.equipement = EquipementView()
        self.alert = AlertView()
        self.coupure = CoupureView()

        self.tabs.addTab(self.dashboard, "Tableau de Bord")
        self.tabs.addTab(self.equipement, "Equipements")
        self.tabs.addTab(self.alert, "Alertes")
        self.tabs.addTab(self.coupure, "Coupures")

        # Ajouter une animation lors du changement d'onglets
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.setCentralWidget(self.tabs)

    def on_tab_changed(self, index):
        """Animation lors du changement d'onglet"""
        current_widget = self.tabs.currentWidget()
        if hasattr(current_widget, 'animate_entry'):
            current_widget.animate_entry()
