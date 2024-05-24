import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy, QSpacerItem
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox, QFrame, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *

##########################################################
#                                                        #
#                  Classe ProduitWidget                  #
#                                                        #
##########################################################
class ProduitWidget(QWidget):
    produit_ajoute = pyqtSignal(str)

    def __init__(self, nom_produit, description_produit, prix_produit):
        super().__init__()
        self.nom_produit = nom_produit

        produit_layout = QHBoxLayout(self)
        produit_layout2 = QVBoxLayout()
        
        image_produit = QLabel()
        produit_layout.addWidget(image_produit)
        image = QPixmap('app2/image/magasin.jpg').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        image_produit.setPixmap(image)

        produit_layout.addLayout(produit_layout2)

        produit_layout2.addWidget(QLabel(f"Produit : {nom_produit}"))
        produit_layout2.addWidget(QLabel(f"Prix : {prix_produit}€"))
        produit_layout2.addWidget(QLabel(f"Description : {description_produit}"))
        produit_layout2.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        ajouter = QPushButton("Ajouter produit")
        ajouter.setFixedHeight(self.height() // 10)
        ajouter.setFixedWidth(self.width() // 5)
        ajouter.setFont(QFont("Arial", 12))
        produit_layout.addWidget(ajouter)

        ajouter.clicked.connect(self.ajouter_produit)

    def ajouter_produit(self):
        self.produit_ajoute.emit(self.nom_produit)





##########################################################
#                                                        #
#                   Classe VueProduit                    #
#                                                        #
##########################################################
class VueProduit(QWidget):
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur  # Stocke une référence au contrôleur
        self.types_produits = set()
        self.produits = []  # Liste de tout les produits

        # Layouts des filtres
        filtre_layout = QVBoxLayout(self)
        filtre_layout2 = QHBoxLayout()
        
        self.filtre_label = QLabel("Filtre")
        filtre_layout.addWidget(self.filtre_label)

        self.filtre1 = QComboBox()
        self.filtre1.addItem("Type de produit")
        self.filtre1.setFixedWidth(self.width() // 3)
        filtre_layout2.addWidget(self.filtre1)
        
        filtre_layout2.addStretch()
        filtre_layout.addLayout(filtre_layout2)
        
        self.filtre_label1 = QLabel(" ")
        filtre_layout.addWidget(self.filtre_label1)

        self.scroll_bar = QScrollArea()  
        filtre_layout.addWidget(self.scroll_bar)  

        self.filtre1.currentIndexChanged.connect(self.filtrer_produits)

    def charger_produits(self, points):
        self.produits = []  # Liste des produits du magasin
        layout_produit = QVBoxLayout()
        for point in points:
            if isinstance(point.get_fonction(), Etagere): # Si la fonction est une etagère alors elle contiens des produits
                for produit in point.get_fonction().get_produits():
                    self.produits.append(produit)  # Ajout le produit à la liste

        self.afficher_produits(self.produits)  # Appel la fonction pour afficher les produits

    def afficher_produits(self, produits):
        layout_produit = QVBoxLayout()
        for produit in produits:
            produit_widget = ProduitWidget(produit.get_nom(), produit.get_description(), produit.get_prix())
            produit_widget.produit_ajoute.connect(self.controleur.ajouter_produit_liste)
            layout_produit.addWidget(produit_widget)
                    
            # Ajoute le type de produit à la QComboBox si ce n'est pas déjà fait
            type_produit = produit.get_type()
            if type_produit not in self.types_produits:
                self.types_produits.add(type_produit)
                self.filtre1.addItem(type_produit)
                    
            ligne_separation = QFrame()
            ligne_separation.setFrameShape(QFrame.Shape.HLine)
            ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
            layout_produit.addWidget(ligne_separation)

        produits_widget = QWidget()
        produits_widget.setLayout(layout_produit)
        self.scroll_bar.setWidget(produits_widget)
        self.scroll_bar.setWidgetResizable(True)

    def filtrer_produits(self):
        self.produits_a_afficher = []
        type_produit = self.filtre1.currentText()
        if type_produit == "Type de produit":
            self.produits_a_afficher = self.produits  # Affiche l'integralité des produits
        else:
            for produit in self.produits :
                if produit.get_type() == type_produit : # Si le produit possède le même type que le filtre alors on l'ajoute
                    self.produits_a_afficher.append(produit)
        
        self.afficher_produits(self.produits_a_afficher) # Appel la fonction pour afficher les produits
        
    # Réinitailise la vue en supprimant tous les layouts    
    def reset_vue(self):
        # Supprime le contenu de la scroll_area
        scroll_content = self.scroll_bar.widget()
        if scroll_content:
            scroll_content.deleteLater()

        # Réinitialise le filtre
        self.filtre1.setCurrentIndex(0)
        self.types_produits.clear()
        self.filtre1.clear()
        self.filtre1.addItem("Type de produit")
        
        # Réinitialise les produits
        self.produits.clear()
        self.produits_a_afficher.clear()