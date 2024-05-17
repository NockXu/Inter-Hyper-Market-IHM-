import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont
from vueProduit import VueProduit
from vueProduit import ProduitWidget
from vuePlan import VuePlan


##########################################################
#                                                        #
#                 Classe vueApplication                  #
#                                                        #
##########################################################
class VueApplication(QMainWindow):
    # constructeur
    def __init__(self, app):
        super().__init__()

        #style d'affichage
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style :
            qss = fichier_style.read()
            self.setStyleSheet(qss)
            
##########################################################
#                                                        #
#                       Layouts                          #
#                                                        #
##########################################################

        # Layout vertical principal
        self.layout_principal = QHBoxLayout()
        centre = QWidget()
        centre.setLayout(self.layout_principal)
        self.setCentralWidget(centre)

        # Layout vertical pour le menu des magasins et de la liste
        self.menu_selection = QVBoxLayout()
        self.layout_principal.addLayout(self.menu_selection)
        
##########################################################
#                                                        #
#                        Wigets                          #
#                                                        #
##########################################################

        # Appel des vues du plan et des produits
        self.produitVue = VueProduit(self)
        self.produitWidget = ProduitWidget(self)
        self.planVue = VuePlan()
        self.planVue.hide() # Permet de cacher la vue du plan

        # ajout d'une barre d'outils
        self.menu_bar = self.menuBar()

        # ajout d'un bouton sauvegarde
        fichier_menu = self.menu_bar.addMenu('Fichier')
        self.action_save = QAction('Enregistrer', self)
        fichier_menu.addAction(self.action_save)

        # ajout d'un bouton réinitialiser
        self.action_reset = QAction('Réinitialiser', self)
        fichier_menu.addAction(self.action_reset)
        
        # Choix des magasins avec un ComboBox
        self.magasin = QComboBox()
        self.magasin.addItem("Choix du magasin")
        self.magasin.addItem("Magasin 1")
        self.magasin.addItem("Magasin 2")
        self.magasin.addItem("Magasin 3")
        self.magasin.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.magasin)

        # Liste de course
        self.liste = QTextEdit()
        self.liste.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.liste)
        
        # Bouton pour voir le plan
        self.ajout_plan = QPushButton("Voir le plan")
        self.ajout_plan.setFixedHeight(self.height() // 8)
        self.ajout_plan.setFont(QFont("Arial", 15))
        self.menu_selection.addWidget(self.ajout_plan)

        self.layout_principal.addWidget(self.produitVue)
        self.layout_principal.addWidget(self.planVue)
        
        # Affichage de l'application
        self.setWindowTitle('Application client')
        self.showMaximized() # Permet de mettre en ecran total

##########################################################
#                                                        #
#                        Signaux                         #
#                                                        #
##########################################################

        self.ajout_plan.clicked.connect(self.changer_vue)
        self.produitWidget.produit_ajoute.connect(self.ajouter_produit_liste)


##########################################################
#                                                        #
#                       Fonctions                        #
#                                                        #
##########################################################

    def changer_vue(self):
        if self.produitVue.isVisible():
            self.produitVue.hide()
            self.ajout_plan.setText("Ajouter des produits")
            self.planVue.show()
        else:
            self.produitVue.show()
            self.planVue.hide()
            self.ajout_plan.setText("Voir le plan")
            
    def ajouter_produit_liste(self, nom_produit):
        self.liste.insertPlainText("- " + nom_produit + "\n")

## Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VueApplication(app)
    sys.exit(app.exec())
