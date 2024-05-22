import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy, QSpacerItem
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox, QFrame, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont

##########################################################
#                                                        #
#                  Classe ProduitWidget                  #
#                                                        #
##########################################################
class ProduitWidget(QWidget):
    produit_ajoute = pyqtSignal(str)

    def __init__(self, nom_produit):
        super().__init__()
        self.nom_produit = nom_produit

        produit_layout = QHBoxLayout(self)
        produit_layout2 = QVBoxLayout()
        
        image_produit = QLabel()
        produit_layout.addWidget(image_produit)
        image = QPixmap('app2/image/magasin.jpg').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        image_produit.setPixmap(image)

        produit_layout.addLayout(produit_layout2)

        description = QLabel("Description")
        produit_layout2.addWidget(QLabel(nom_produit))
        produit_layout2.addWidget(description)
        produit_layout2.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        ajouter = QPushButton("Ajouter produit")
        ajouter.setFixedHeight(self.height() // 10)
        ajouter.setFixedWidth(self.width() // 5)
        ajouter.setFont(QFont("Arial", 12))
        produit_layout.addWidget(ajouter)

        ajouter.clicked.connect(self.ajouter_produit)

    def ajouter_produit(self):
        self.produit_ajoute.emit(self.nom_produit)


class VueProduit(QWidget):
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur  # Stocke une référence au contrôleur

        # Layouts des filtres
        filtre_layout = QVBoxLayout(self)
        filtre_layout2 = QHBoxLayout()
        
        self.filtre_label = QLabel("Filtre")
        filtre_layout.addWidget(self.filtre_label)

        self.filtre1 = QComboBox()
        self.filtre1.addItem("Type de produit")
        self.filtre1.addItem("Option 2")
        self.filtre1.setFixedWidth(self.width() // 3)
        filtre_layout2.addWidget(self.filtre1)
        
        filtre_layout2.addStretch()
        filtre_layout.addLayout(filtre_layout2)
        
        self.filtre_label1 = QLabel(" ")
        filtre_layout.addWidget(self.filtre_label1)

        self.scroll_bar = QScrollArea()  
        filtre_layout.addWidget(self.scroll_bar)  
        
    def charger_produits(self, fichier_produits):
        layout_produit = QVBoxLayout()  # Créez un nouveau layout pour les produits
        with open(fichier_produits, 'r') as file:
            for line in file:
                if '[' in line and ']' in line:
                    continue
                else:
                    nom_produit = line.strip()
                    produit_widget = ProduitWidget(nom_produit)
                    produit_widget.produit_ajoute.connect(self.controleur.ajouter_produit_liste)
                    layout_produit.addWidget(produit_widget)
                    
                    ligne_separation = QFrame()
                    ligne_separation.setFrameShape(QFrame.Shape.HLine)
                    ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
                    layout_produit.addWidget(ligne_separation)
        
        # Ajoutez le layout_produit à la scroll_bar
        produits = QWidget()
        produits.setLayout(layout_produit)
        self.scroll_bar.setWidget(produits)
        self.scroll_bar.setWidgetResizable(True)
        
    # Réinitailise la vue en supprimant tous les layouts    
    def reset_vue(self):
        # Supprime le contenu de la scroll_area
        scroll_content = self.scroll_bar.widget()
        if scroll_content:
            scroll_content.deleteLater()

        # Réinitialise les filtres
        self.filtre1.setCurrentIndex(0)
