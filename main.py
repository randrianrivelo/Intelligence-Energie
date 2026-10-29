import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.main_controller import MainController

app = QApplication(sys.argv)
window = MainWindow()
controller = MainController(window)
window.show()
sys.exit(app.exec_())
