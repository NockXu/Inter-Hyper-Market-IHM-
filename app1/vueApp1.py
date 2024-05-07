import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Barre d'outils
        self.toolbar = QToolBar('')
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # Ajouter des actions à la barre d'outils
        self.action_nouveau = QAction('Nouveau', self)
        self.toolbar.addAction(self.action_nouveau)

        self.action_ouvrir = QAction('Ouvrir', self)
        self.toolbar.addAction(self.action_ouvrir)

        self.action_enregistrer = QAction('Enregistrer', self)
        self.toolbar.addAction(self.action_enregistrer)

        self.action_supprimer = QAction('Supprimer', self)
        self.toolbar.addAction(self.action_supprimer)

        # Ajouter un espace extensible à gauche de la barre d'outils pour aligner les boutons à gauche
        spacer_left = QWidget()
        spacer_left.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer_left)

        # Ajouter un espace extensible à droite de la barre d'outils pour aligner le bouton à droite
        spacer_right = QWidget()
        spacer_right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer_right)

        self.action_reset = QAction('Réinitialiser', self)
        self.toolbar.addAction(self.action_reset)
        
        # layout 
        
        self.layout_left : QVBoxLayout = QVBoxLayout()
        self.lab1 : QLabel = QLabel('Widget gauche')
        self.layout_left.addWidget(self.lab1)
        
        self.layout_right : QHBoxLayout = QHBoxLayout()
        self.lab2 : QLabel = QLabel('Widget droit')
        self.layout_right.addWidget(self.lab2) 

        self.layout_groupe : QHBoxLayout = QHBoxLayout()

        # Ajout des layouts à layout_groupe
        self.layout_groupe.addLayout(self.layout_left)
        self.layout_groupe.addLayout(self.layout_right)
        
        self.widget_centre = QWidget()
        self.widget_centre.setLayout(self.layout_groupe)
        self.setCentralWidget(self.widget_centre)

        # Paramètres d'affichage
        self.setWindowTitle('INTER-HYPER-MARKET')
        self.showMaximized()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
