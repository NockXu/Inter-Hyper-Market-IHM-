import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *

class Init(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Boutons
        self.nouveau = QPushButton('Nouveau Projet')
        self.ouvrir = QPushButton('Ouvrir')

        # Layout pour les boutons
        layout_boutons = QHBoxLayout()
        layout_boutons.addWidget(self.nouveau)
        layout_boutons.addWidget(self.ouvrir)
        layout_boutons.setContentsMargins(0, 0, 0, 0)

        # Widget pour les boutons
        boutons_widget = QWidget()
        boutons_widget.setLayout(layout_boutons)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(boutons_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)

        # Affichage
        self.setWindowTitle('INTER-HYPER-MARKET')
        self.showMaximized()
        self.show()
        
        # Action
        self.nouveau.clicked.connect(self.lancer)
        self.ouvrir.clicked.connect(self.lancer)
        
        
    def lancer(self):
        from vueApp1 import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        
        # Fermer l'interface une fois que la vue est laancer
        if self.lancer:
            self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Init()
    sys.exit(app.exec())