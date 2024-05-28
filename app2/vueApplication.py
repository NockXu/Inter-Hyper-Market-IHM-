import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox, QFileDialog, QSpacerItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont
from vueProduit import VueProduit
from vuePlan import VuePlan


##########################################################
#                                                        #
#                 Classe vueApplication                  #
#                                                        #
##########################################################
class VueApplication(QMainWindow):
    produit_ajoute = pyqtSignal(str)

    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur  # Stocke une référence au contrôleur

        # Style d'affichage
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)

##########################################################
#                                                        #
#                       Layouts                          #
#                                                        #
##########################################################

        self.layout_principal = QHBoxLayout()
        centre = QWidget()
        centre.setLayout(self.layout_principal)
        self.setCentralWidget(centre)

        self.menu_selection = QVBoxLayout()
        self.layout_principal.addLayout(self.menu_selection)

        # Layout de la liste des produits séléctionner
        self.liste_layout = QVBoxLayout()

##########################################################
#                                                        #
#                          Vue                           #
#                                                        #
##########################################################

        self.produitVue = VueProduit(self.controleur)
        self.planVue = VuePlan()
        self.planVue.hide()


##########################################################
#                                                        #
#                        Widgets                         #
#                                                        #
##########################################################
             
        # Barre d'outils qui permet d'ajouter des fonctionnalités 
        # supplémentaires à l'application
        self.menu_bar = self.menuBar()
        fichier_menu = self.menu_bar.addMenu('Options')


        # Option de choix du magasin, permet à l'utilisateur de 
        # choisir le magasin de plusieurs manières
        self.ouvrir = QAction('Choisir magasin', self)
        fichier_menu.addAction(self.ouvrir)


        # Option qui supprime toutes les modifications et remet l'application 
        # dans l'état d'origine, comme si elle venait d'être lancée
        self.action_reset = QAction('Réinitialiser', self)
        fichier_menu.addAction(self.action_reset)


        # Bouton de choix du magasin
        self.magasin = QPushButton("Choisir magasin")
        self.magasin.setFixedWidth(self.width() // 3) # Redimensionne la largeur du bouton à un tiers de la taille de l'écran
        self.menu_selection.addWidget(self.magasin)


        # Zone de scroll qui permet de se deplacer de manière vertical
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.liste_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.scroll_area)


        # Ajout d'un espace pour que les produits s'ajoute en haut de la liste 
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.liste_layout.addItem(self.spacer)


        # Bouton qui à pour effet de vider entièrement la liste des produits séléctionné
        self.supp = QPushButton("Supprimer la liste")
        self.supp.setFont(QFont("Arial", 12))
        self.menu_selection.addWidget(self.supp)
        
        
        # Ligne de separation 
        separation = QFrame()
        separation.setFrameShape(QFrame.Shape.HLine)
        separation.setFrameShadow(QFrame.Shadow.Sunken)
        self.menu_selection.addWidget(separation)


        # Bouton qui affiche la vu du plan avec le chemin le plus optimisé 
        self.ajout_plan = QPushButton("Voir le plan")
        self.ajout_plan.setFixedHeight(self.height() // 8) # Redimensionne la largeur du bouton à un huitième de la taille de l'écran
        self.ajout_plan.setFont(QFont("Arial", 15))
        self.menu_selection.addWidget(self.ajout_plan)
        
        
        # Ajout des vu à l'affichage 
        self.layout_principal.addWidget(self.produitVue)
        self.layout_principal.addWidget(self.planVue)


        # Affichage
        self.setWindowTitle('Application client')
        self.showMaximized() # Affiche la fenêtre à la taille de l'ecran
    

## Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VueApplication(app)
    sys.exit(app.exec())