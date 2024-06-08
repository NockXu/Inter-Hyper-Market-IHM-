import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QGridLayout, QColorDialog, QHBoxLayout, QFrame
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QColor
from valeurAdjuster import ValeurAdjuster
from frame import LineFrame
from TableWidget import TableWidget
from fonctionRect import FonctionRect

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class VueDockMenuCarre(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialisation des composants de layout_carre
        self.nb_carre_x_label = QLabel('Nombre de carrés en hauteur')
        self.nb_carre_x = ValeurAdjuster(50, False)
        self.nb_carre_y_label = QLabel('Nombre de carrés en longueur')
        self.nb_carre_y = ValeurAdjuster(50, False)
        self.carre_button = QPushButton('Ajouter plan')

        # Initialisation des lignes de séparation
        self.carreFonc = LineFrame()
        self.foncRay = LineFrame()

        # Layout pour les options de carrés
        self.layout_carre = QVBoxLayout()
        self.layout_carre.addWidget(self.nb_carre_x_label)
        self.layout_carre.addWidget(self.nb_carre_x)
        self.layout_carre.addWidget(self.nb_carre_y_label)
        self.layout_carre.addWidget(self.nb_carre_y)
        self.layout_carre.addWidget(self.carre_button)
        self.layout_carre.addSpacing(5)
        self.layout_carre.addWidget(self.carreFonc)
        self.layout_carre.addSpacing(5)
        
        self.tableRayon = TableWidget()
        
        # Ajout des fonctions des rectangles
        self.fonction = FonctionRect()

        # Layout principal
        self.layout_dock = QVBoxLayout()
        self.layout_dock.addLayout(self.layout_carre)
        self.layout_dock.addWidget(self.fonction)
        self.layout_dock.addSpacing(5)
        self.layout_dock.addWidget(self.foncRay)
        self.layout_dock.addSpacing(5)
        self.layout_dock.addWidget(self.tableRayon)

        self.setLayout(self.layout_dock)
        self.selected_color = QColor('white')

    def carre_couleur(self, color):
        """
        Crée un carré de couleur avec une taille fixe.
        """
        square = QWidget()
        square.setFixedSize(QSize(50, 50))
        square.setStyleSheet(f'background-color: {color}; border: 5px solid black; border-radius: 10px;')
        return square
        
    def getTailleCarre(self):
        """
        Permet de recuperer la taille d'un carre
        """
        return int(self.nb_carre_x.valeur), int(self.nb_carre_y.valeur)

    def reset(self):
        """
        Permet de reintialiser l'affichage
        """
        self.nb_carre_x.clear()
        self.nb_carre_y.clear()
        self.tableRayon.clear()
        if not self.fonction.mode_fonction:
            self.fonction.toggle_mode()


    def toggle_grid(self):
        if self.bouton_fonction.text() == 'Activer ?':
            self.bouton_fonction.setText('Desactiver?')
        else:
            self.bouton_fonction.setText('Activer ?')
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = VueDockMenuCarre()
    mainWin.setWindowTitle('test')
    mainWin.show()
    sys.exit(app.exec())

