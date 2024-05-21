import sys
import json
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

    def __init__(self, nom_produit, description, prix, icone):
        super().__init__()
        self.nom_produit = nom_produit

##########################################################
#                                                        #
#                        Layout                          #
#                                                        #
##########################################################

        produit_layout = QHBoxLayout(self)
        produit_layout2 = QVBoxLayout()
        
##########################################################
#                                                        #
#                        Widgets                         #
#                                                        #
##########################################################

        image_produit = QLabel()
        produit_layout.addWidget(image_produit)
        image = QPixmap('app2/image/magasin.jpg').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        image_produit.setPixmap(image)
        #if icone:
        #    image = QPixmap(icone).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        #    image_produit.setPixmap(image)

        produit_layout.addLayout(produit_layout2)

        produit_layout2.addWidget(QLabel(f"Produit: {nom_produit}"))
        produit_layout2.addWidget(QLabel(f"Description: {description}"))
        produit_layout2.addWidget(QLabel(f"Prix: {prix} €"))
        produit_layout2.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        ajouter = QPushButton("Ajouter produit")
        ajouter.setFixedHeight(self.height() // 10)
        ajouter.setFixedWidth(self.width() // 5)
        ajouter.setFont(QFont("Arial", 12))
        produit_layout.addWidget(ajouter)

##########################################################
#                                                        #
#                        Signaux                         #
#                                                        #
##########################################################

        ajouter.clicked.connect(self.ajouter_produit)

##########################################################
#                                                        #
#                       Fonctions                        #
#                                                        #
##########################################################

    def ajouter_produit(self):
        self.produit_ajoute.emit(self.nom_produit)

































##########################################################
#                                                        #
#                   Classe VueProduit                    #
#                                                        #
##########################################################
class VueProduit(QWidget):
    def __init__(self, vue_application):
        super().__init__()
        self.vue_application = vue_application  # Stocke une référence à VueApplication

##########################################################
#                                                        #
#                       Layouts                          #
#                                                        #
##########################################################

        # Layouts des filtres
        filtre_layout = QVBoxLayout(self)
        filtre_layout2 = QHBoxLayout()
        
##########################################################
#                                                        #
#                        Widgets                         #
#                                                        #
##########################################################

        self.filtre_label = QLabel("Filtre")
        filtre_layout.addWidget(self.filtre_label)

        self.filtre1 = QComboBox()
        self.filtre1.addItem("Type de produit")
        self.filtre1.addItem("Option 2")
        self.filtre1.setFixedWidth(self.width() // 3)
        filtre_layout2.addWidget(self.filtre1)

        self.filtre2 = QComboBox()
        self.filtre2.addItem("Rayon")
        self.filtre2.addItem("Option B")
        self.filtre2.setFixedWidth(self.width() // 3)
        filtre_layout2.addWidget(self.filtre2)
        
        filtre_layout2.addStretch()
        filtre_layout.addLayout(filtre_layout2)
        
        self.filtre_label1 = QLabel(" ")
        filtre_layout.addWidget(self.filtre_label1)

        self.scroll_bar = QScrollArea()
        filtre_layout.addWidget(self.scroll_bar)  # Ajoutez la scroll_bar au layout principal
        
        
##########################################################
#                                                        #
#                       Fonctions                        #
#                                                        #
##########################################################

    def charger_produits(self, fichier_produits):
        layout_produit = QVBoxLayout()  # Créez un nouveau layout pour les produits
        with open(fichier_produits, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                fonction = item.get('fonction', {})
                produits = fonction.get('produits', [])
                for produit in produits:
                    nom_produit = produit.get('nom', 'N/A')
                    description = produit.get('description', 'Pas de description')
                    prix = produit.get('prix', 0)
                    icone = produit.get('icone', '')
                    produit_widget = ProduitWidget(nom_produit, description, prix, icone)
                    produit_widget.produit_ajoute.connect(self.vue_application.ajouter_produit_liste)
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
        
    def reset_vue(self):
        # Supprime le contenu de la scroll_area
        scroll_content = self.scroll_bar.widget()
        if scroll_content:
            scroll_content.deleteLater()

        # Réinitialise les filtres
        self.filtre1.setCurrentIndex(0)
        self.filtre2.setCurrentIndex(0)


class VueApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vue Application')
        self.setGeometry(100, 100, 800, 600)

        # Instance of VueProduit
        self.vue_produit = VueProduit(self)
        self.setCentralWidget(self.vue_produit)

        # ToolBar and Menu
        self.createToolBar()
        self.show()

    def createToolBar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        load_action = QAction(QIcon('load.png'), 'Load Products', self)
        load_action.triggered.connect(self.load_products)
        toolbar.addAction(load_action)

    def load_products(self):
        # Here you would have code to select a JSON file
        self.vue_produit.charger_produits('path_to_your_json_file.json')

    def ajouter_produit_liste(self, nom_produit):
        print(f"Produit ajouté: {nom_produit}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vue_app = VueApplication()
    sys.exit(app.exec())
