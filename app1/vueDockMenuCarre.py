import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QGridLayout, QColorDialog
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon

class VueDockMenuCarre(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialisation des composants de layout_carre
        self.nb_carre_x_label = QLabel('Nombre de carre en hauteur')
        self.nb_carre_x = QLineEdit()
        self.nb_carre_y_label = QLabel('Nombre de carre en longueur')
        self.nb_carre_y = QLineEdit()
        self.carre_button = QPushButton('Carre')

        # Layout pour les options de carrés
        self.layout_carre = QVBoxLayout()
        self.layout_carre.addWidget(self.nb_carre_x_label)
        self.layout_carre.addWidget(self.nb_carre_x)
        self.layout_carre.addWidget(self.nb_carre_y_label)
        self.layout_carre.addWidget(self.nb_carre_y)
        self.layout_carre.addWidget(self.carre_button)
        self.layout_carre.addStretch(1)

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

        self.nom_rayon = QLineEdit()
        self.nom_rayon.setPlaceholderText('Nom')
        self.couleur_rayon = QPushButton('Couleur')
        self.couleur_rayon.clicked.connect(self.open_color_dialog)
        self.ajout_rayon = QPushButton(QIcon('./images/add.svg'), 'Add', self)

        self.layout_rayon = QGridLayout()
        self.layout_rayon.addWidget(self.nom_rayon, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_rayon.addWidget(self.couleur_rayon, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_rayon.addWidget(self.ajout_rayon, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        
        self.layout_fonction = QVBoxLayout()
        self.layout_fonction.addWidget(self.bouton_fonction)
        self.layout_fonction.addLayout(self.layout_form)
        self.layout_fonction.addStretch(1) 

        # Layout principal
        self.layout_dock = QVBoxLayout()
        self.layout_dock.addLayout(self.layout_carre)
        self.layout_dock.addLayout(self.layout_fonction)
        self.layout_dock.addLayout(self.layout_rayon)

        self.setLayout(self.layout_dock)

    def carre_couleur(self, color):
        """Crée un carré de couleur avec une taille fixe."""
        square = QWidget()
        square.setFixedSize(QSize(50, 50))
        square.setStyleSheet(f'background-color: {color}; border: 5px solid black; border-radius: 10px;')
        return square
    
    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(f'Couleur sélectionnée: {color.name()}')

    def getTailleCarre(self):
        return int(self.nb_carre_x.text()), int(self.nb_carre_y.text())

    def reset(self):
        self.nb_carre_x.clear()
        self.nb_carre_y.clear()