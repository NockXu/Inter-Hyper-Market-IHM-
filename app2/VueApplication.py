import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont
from VueProduit import VueProduit
from VuePlan import VuePlan


##########################################################
#                                                        #
#                 Classe vueApplication                  #
#                                                        #
##########################################################
class VueApplication(QMainWindow):
    # constructeur
    def __init__(self):
        
        #style d'affichage
        self.app = QApplication(sys.argv)
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style :
            qss = fichier_style.read()
            self.app.setStyleSheet(qss)

        super().__init__()

##########################################################
#                                                        #
#                        Layouts                         #
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
#                        Widgets                         #
#                                                        #
##########################################################

        self.produitVue = VueProduit()

        # ajout d'une barre d'outils
        self.toolbar = QToolBar('')
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # ajout d'un bouton sauvegarde
        self.action_save = QAction('Enregistrer', self)
        self.toolbar.addAction(self.action_save)

        # ajout d'un bouton réinitialiser
        self.toolbar.addSeparator() 
        self.icon2 = QAction('Réinitialiser', self)
        self.toolbar.addAction(self.icon2)
        
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


##########################################################
#                                                        #
#                          Show                          #
#                                                        #
##########################################################

        # Affichage de l'application
        self.setWindowTitle('Application client')
        self.showMaximized() # Permet de mettre en ecran total
        
        
        

        

## Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":

    print(f' --- main --- ')

    fenetre = VueApplication()
    sys.exit(fenetre.app.exec())