from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ValeurAdjuster(QWidget):
    def __init__(self, max : int, autoriserNegatif : bool = True):
        super().__init__()

        # Initialisation du maximum
        self.max = max
        
        # Initialisation du booléen qui sert à savoir si le compteur peu aller dans le négatif
        self.autoriserNegatif = autoriserNegatif
        
        # Initialisation de la valeur
        self.valeur = 0

        # Création du layout horizontal
        self.layout = QHBoxLayout()

        self.bouttonDiminuer = QPushButton(QIcon("app1/images/sub.svg"), "", self)
        self.bouttonDiminuer.clicked.connect(self.decrease_valeur)
        self.bouttonDiminuer.setFixedWidth(50)

        self.bouttonAugmenter = QPushButton(QIcon("app1/images/add.svg"), "", self)
        self.bouttonAugmenter.clicked.connect(self.increase_valeur)
        self.bouttonAugmenter.setFixedWidth(50)

        self.valeurEntrer = QLineEdit(self)
        self.valeurEntrer.setFixedWidth(60)
        self.valeurEntrer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.valeurEntrer.setText(str(self.valeur))
        self.valeurEntrer.textChanged.connect(self.set_valeur_from_change)

        # Ajout des widgets au layout
        self.layout.addWidget(self.bouttonDiminuer)
        self.layout.addWidget(self.valeurEntrer)
        self.layout.addWidget(self.bouttonAugmenter)

        # Configuration du layout principal
        self.setLayout(self.layout)

    def clear(self) -> None:
        self.valeur = 0
        self.updateValeur()
    
    def increase_valeur(self):
        if self.valeur < self.max:
            self.valeur += 1
            self.updateValeur()

    def decrease_valeur(self):
        if self.valeur > 0 :
            self.valeur -= 1
        elif self.autoriserNegatif and self.valeur > -self.max:
            self.valeur -= 1
        self.updateValeur()

    def set_valeur_from_change(self):
        try:
            self.valeur = int(self.valeurEntrer.text())
            if self.valeur > self.max:
                self.valeur = self.max
            self.updateValeur()
        except ValueError:
            self.valeurEntrer.setText(str(self.valeur))

    def updateValeur(self):
        self.valeurEntrer.setText(str(self.valeur))
        
    def set_valeur(self, valeur : int) -> None:
        self.valeur = valeur
        if self.valeur > self.max:
            self.valeur = self.max
        self.updateValeur()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ValeurAdjuster(10, False)
    mainWin.setWindowTitle('valeur Adjuster')
    mainWin.show()
    sys.exit(app.exec())