from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class VueDockMenuCarre(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_dock = QVBoxLayout()

        self.nb_carre_x_label : QLabel = QLabel('Nombre de carre en hauteur')
        self.nb_carre_x : QLineEdit = QLineEdit()

        self.nb_carre_y_label : QLabel = QLabel('Nombre de carre en longueur')
        self.nb_carre_y : QLineEdit = QLineEdit()

        self.carre_button : QPushButton = QPushButton('Carre')

        self.layout_dock.addWidget(self.nb_carre_x_label)
        self.layout_dock.addWidget(self.nb_carre_x)

        self.layout_dock.addWidget(self.nb_carre_y_label)
        self.layout_dock.addWidget(self.nb_carre_y)

        self.layout_dock.addWidget(self.carre_button)

        self.layout_dock.addStretch(1)
        self.setLayout(self.layout_dock)
        
    def getTailleCarre(self):
        return int(self.nb_carre_x.text()), int(self.nb_carre_y.text())