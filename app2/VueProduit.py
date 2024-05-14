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
    def __init__(self):
        super().__init__()
        
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

        for i in range(70):
                produit_widget = QWidget()
                layout = QHBoxLayout(produit_widget)
                produit_layout = QVBoxLayout()
                
                image_produit = QLabel()
                layout.addWidget(image_produit)
                pixmap = QPixmap('./image/magasin.jpg')
                image_produit.setPixmap(pixmap)

                
                nom_produit = QLabel(f"Produit {i+1}")
                description = QLabel("Description")                
                produit_layout.addWidget(nom_produit)
                produit_layout.addWidget(description)
                layout.addLayout(produit_layout)
                
                ajouter = QPushButton("Ajouter produit")
                ajouter.setFixedHeight(self.height() // 15)
                ajouter.setFixedWidth(self.width() // 5)
                layout.addWidget(ajouter)
                
                layout_produit.addWidget(produit_widget)
                
                 # Ajouter une ligne de séparation
                if i < 69:  # Ne pas ajouter de ligne de séparation après le dernier produit
                    line = QFrame()
                    line.setFrameShape(QFrame.Shape.HLine)
                    line.setFrameShadow(QFrame.Shadow.Sunken)
                    layout_produit.addWidget(line)
    
        produits.setLayout(layout_produit)
        scroll_bar.setWidgetResizable(True)

        
if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VueProduit()
    fenetre.show()
    sys.exit(app.exec())