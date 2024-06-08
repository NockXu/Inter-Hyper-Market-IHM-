from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from imageSelector import *

class VueDockMenuOutil(QWidget):
    
    nomMagasinChanger = pyqtSignal(str)
    nomProjetChanger = pyqtSignal(str)
    auteurChanger = pyqtSignal(str)
    dateChanger = pyqtSignal(QDate)
    addresseChanger = pyqtSignal(str)
    loadPressed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_dock = QVBoxLayout()

        self.load_plan_button = QPushButton('Charger un plan')
        self.load_plan_button.clicked.connect(self.load)

        self.nom_projet_label = QLabel("Nom de projet :")
        self.nom_projet = QLineEdit()
        self.nom_projet.textChanged.connect(self.on_nom_projet_changed)

        self.nom_magasin_label = QLabel('Nom du magasin :')
        self.nom_magasin = QLineEdit()
        self.nom_magasin.textChanged.connect(self.on_nom_magasin_changed)

        self.auteur_label = QLabel('Auteur :')
        self.auteur = QLineEdit()
        self.auteur.textChanged.connect(self.on_auteur_changed)

        self.date_label = QLabel('Date de création :')
        self.date = QDateEdit(calendarPopup=True)
        self.date.setDate(QDate.currentDate())
        self.date.dateChanged.connect(self.on_date_changed)

        self.adresse_label = QLabel('Adresse du magasin :')
        self.adresse = QLineEdit()
        self.adresse.textChanged.connect(self.on_adresse_changed)
        
        self.image_label = QLabel("Selection de l'image :")
        self.image = ImageSelector()

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
        self.layout_dock.addWidget(self.image_label)
        self.layout_dock.addWidget(self.image)

        self.setLayout(self.layout_dock)
    
    def reset(self):
        self.nom_projet.clear()
        self.nom_magasin.clear()
        self.auteur.clear()
        self.date.setDate(QDate.currentDate())
        self.adresse.clear()
        self.image.clear()
    
    def on_nom_projet_changed(self, text):
        self.nomProjetChanger.emit(text)
    
    def on_nom_magasin_changed(self, text):
        self.nomMagasinChanger.emit(text)
    
    def on_auteur_changed(self, text):
        self.auteurChanger.emit(text)
    
    def on_date_changed(self, date):
        self.dateChanger.emit(date)
    
    def on_adresse_changed(self, text):
        self.addresseChanger.emit(text)
        
    def load(self):
        self.loadPressed.emit()
