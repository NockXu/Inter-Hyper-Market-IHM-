import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QGridLayout, QColorDialog, QHBoxLayout, QFrame
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QColor
from valeurAdjuster import ValeurAdjuster
from frame import LineFrame
from TableWidget import TableWidget

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


        # Initialisation des composants de layout_fonction
        self.bouton_fonction = QPushButton('Activer ?')
        self.couleur_chemin = self.carre_couleur('red')
        self.couleur_entree = self.carre_couleur('green')
        self.couleur_etagere = self.carre_couleur('blue')
        self.couleur_chemin_label = QLabel('chemin')
        self.couleur_entree_label = QLabel('entrée')
        self.couleur_etagere_label = QLabel('étagère')

        # Layout pour les fonctionnalités
        self.layout_fonction = QVBoxLayout()
        self.layout_form = QFormLayout()

        self.layout_fonction.addWidget(self.bouton_fonction)

        self.layout_form.addRow(self.couleur_chemin, self.couleur_chemin_label)
        self.layout_form.addRow(self.couleur_entree, self.couleur_entree_label)
        self.layout_form.addRow(self.couleur_etagere, self.couleur_etagere_label)
        self.layout_form.setVerticalSpacing(20)
        self.layout_form.setHorizontalSpacing(50)
        
        self.tableRayon = TableWidget()

        self.layout_fonction = QVBoxLayout()
        self.layout_fonction.addWidget(self.bouton_fonction)
        self.layout_fonction.addLayout(self.layout_form)

        # Layout principal
        self.layout_dock = QVBoxLayout()
        self.layout_dock.addLayout(self.layout_carre)
        self.layout_dock.addLayout(self.layout_fonction)
        self.layout_dock.addSpacing(5)
        self.layout_dock.addWidget(self.foncRay)
        self.layout_dock.addSpacing(5)
        self.layout_dock.addWidget(self.tableRayon)

        self.setLayout(self.layout_dock)
        self.selected_color = QColor('white')

        self.bouton_fonction.clicked.connect(self.toggle_grid)

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
        # Supprimer tous les widgets de rayons
        while self.rayons_layout.count():
            child = self.rayons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

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

