from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class VueDockMenuOutil(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_dock = QVBoxLayout()

        self.load_plan_button = QPushButton('Charger un plan')

        self.nom_projet_label = QLabel("Nom de projet :")
        self.nom_projet = QLineEdit()

        self.nom_magasin_label = QLabel('Nom du magasin :')
        self.nom_magasin = QLineEdit()

        self.auteur_label = QLabel('Auteur :')
        self.auteur = QLineEdit()

        self.date_label = QLabel('Date de création :')
        self.date = QDateEdit(calendarPopup=True)
        self.date.setDate(QDate.currentDate())

        self.adresse_label = QLabel('Adresse du magasin :')
        self.adresse = QLineEdit()

        self.layout_dock.addWidget(self.load_plan_button)
        self.layout_dock.addWidget(self.nom_projet_label)
        self.layout_dock.addWidget(self.nom_projet)
        self.layout_dock.addWidget(self.nom_magasin_label)
        self.layout_dock.addWidget(self.nom_magasin)
        self.layout_dock.addWidget(self.auteur_label)
        self.layout_dock.addWidget(self.auteur)
        self.layout_dock.addWidget(self.date_label)
        self.layout_dock.addWidget(self.date)
        self.layout_dock.addWidget(self.adresse_label)
        self.layout_dock.addWidget(self.adresse)

        self.layout_dock.addStretch(1)
        self.setLayout(self.layout_dock)
        
    def get_load_plan_button(self):
        return self.load_plan_button
    
    def reset(self):
        self.nom_projet.clear()
        self.nom_magasin.clear()
        self.auteur.clear()
        self.date.setDate(QDate.currentDate())
        self.adresse.clear()