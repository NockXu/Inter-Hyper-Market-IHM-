import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy, QFrame
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox, QScrollArea, QSpacerItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont

##########################################################
#                                                        #
#                    Classe vueProduit                   #
#                                                        #
##########################################################
class VueProduit(QWidget):
    # Signal personnalisé qui émet le nom du produit lorsqu'il est ajouté
    produit_ajoute = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        # Liste pour stocker les noms des produits
        self.noms_produits = []
        ##########################################################
        #                                                        #
        #                        Layouts                         #
        #                                                        #
        ##########################################################
        filtre_layout = QVBoxLayout()
        self.setLayout(filtre_layout)
        filtre_layout2 = QHBoxLayout()
        
        ##########################################################
        #                                                        #
        #                        Widgets                         #
        #                                                        #
        ##########################################################
        
        self.filtre_label = QLabel("Filtre")
        filtre_layout.addWidget(self.filtre_label)

        # Filtre qui vise les types de produits
        self.filtre1 = QComboBox()
        self.filtre1.addItem("Type de produit")
        self.filtre1.addItem("Option 2")
        self.filtre1.setFixedWidth(self.width() // 3)
        filtre_layout2.addWidget(self.filtre1)

        # Filtre qui vise les rayons
        self.filtre2 = QComboBox()
        self.filtre2.addItem("Rayon")
        self.filtre2.addItem("Option B")
        self.filtre2.setFixedWidth(self.width() // 3)
        filtre_layout2.addWidget(self.filtre2)
        
        
        filtre_layout2.addStretch()
        filtre_layout.addLayout(filtre_layout2)
        
        self.filtre_label1 = QLabel(" ")
        filtre_layout.addWidget(self.filtre_label1)

        # Ajout d'une bare pour se deplacer verticalement dans la liste des produits
        scroll_bar = QScrollArea()
        filtre_layout.addWidget(scroll_bar)
        
        produits = QWidget()
        scroll_bar.setWidget(produits)
        layout_produit = QVBoxLayout(produits)

        with open('liste_produits.txt', 'r') as file:
            for line in file:
                # Ignorer les noms entre crochets
                if '[' in line and ']' in line:
                    continue
                else:
                    produit_widget = QWidget()
                    layout = QHBoxLayout(produit_widget)
                    produit_layout = QVBoxLayout()
                    
                    image_produit = QLabel()
                    layout.addWidget(image_produit)
                    image = QPixmap('app2/image/magasin.jpg').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    image_produit.setPixmap(image)

                    # Extraire le nom du produit en supprimant les espaces et les sauts de ligne
                    nom_produit = line.strip()
                    self.noms_produits.append(nom_produit)  # Ajouter le nom du produit à la liste
                    description = QLabel("Description")
                    produit_layout.addWidget(QLabel(nom_produit))  # Utilisation directe de nom_produit
                    produit_layout.addWidget(description)
                    layout.addLayout(produit_layout)
                    layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

                    ajouter = QPushButton("Ajouter produit")
                    ajouter.setFixedHeight(self.height() // 10)
                    ajouter.setFixedWidth(self.width() // 5)
                    ajouter.setFont(QFont("Arial", 12))
                    layout.addWidget(ajouter)
                    
                    layout_produit.addWidget(produit_widget)
                    
                     # Ajouter une ligne de séparation
                    line = QFrame()
                    line.setFrameShape(QFrame.Shape.HLine)
                    line.setFrameShadow(QFrame.Shadow.Sunken)
                    layout_produit.addWidget(line)

##########################################################
#                                                        #
#                        Signaux                         #
#                                                        #
##########################################################
                    
                    # Connecter le clic sur le bouton "Ajouter produit" à la méthode ajouter_produit
                    ajouter.clicked.connect(self.ajouter_produit)

        produits.setLayout(layout_produit)
        scroll_bar.setWidgetResizable(True)

##########################################################
#                                                        #
#                       Fonctions                        #
#                                                        #
##########################################################

    def ajouter_produit(self):
        # Récupérer le nom du produit associé au bouton cliqué
        sender_button = self.sender()  # Obtenir le bouton qui a émis le signal
        produit_widget = sender_button.parentWidget()  # Obtenir le widget parent (produit_widget)
        nom_produit = produit_widget.findChild(QLabel).text()  # Récupérer le texte du QLabel (nom du produit)

        # Émettre le signal avec le nom du produit
        self.produit_ajoute.emit(nom_produit)


        
        
        
if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VueProduit()
    fenetre.show()
    sys.exit(app.exec())
