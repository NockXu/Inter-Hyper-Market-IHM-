import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication

# -----------------------------------------------------------------------------
# --- class Interface
# -----------------------------------------------------------------------------
class vueClient(QMainWindow):
    # constructeur
    def __init__(self):
        
        #style d'affichage
        self.app = QApplication(sys.argv)
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style :
            qss = fichier_style.read()
            self.app.setStyleSheet(qss)

        super().__init__()

        # layout vertical --> principal layout
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        
##########################################################
#                                                        #
#                     Central Widget                     #
#                                                        #
##########################################################

        # Créer un Widget central pour y introduire un layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

##########################################################
#                                                        #
#                        Layouts                         #
#                                                        #
##########################################################

        # Layout vertical principal
        self.layout_principal = QVBoxLayout()
        centre = QWidget()
        centre.setLayout(self.layout_principal)
        self.setCentralWidget(centre)

        # Layout vertical pour le menu hamburger et la zone de texte
        self.menu_selection = QVBoxLayout()
        self.layout_principal.addLayout(self.menu_selection)

        self.magasin = QComboBox()
        self.magasin.addItem("Choix du magasin")
        self.magasin.addItem("Magasin 1")
        self.magasin.addItem("Magasin 2")
        self.magasin.addItem("Magasin 3")
        self.menu_selection.addWidget(self.magasin)

        # Liste de course
        self.liste = QTextEdit()
        self.menu_selection.addWidget(self.liste)


##########################################################
#                                                        #
#                        Widgets                         #
#                                                        #
##########################################################

        # ajout d'une barre d'outils
        self.toolbar = QToolBar('')
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # ajout d'un bouton sauvegarde
        self.action_save = QAction('Enregistrer', self)
        self.toolbar.addAction(self.action_save)

        # ajout d'un bouton réinitialiser
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) #Permet de modifier l'espace créer pour que l'icone soit à droite
        self.toolbar.addWidget(spacer)
        self.icon2 = QAction('Réinitialiser', self)
        self.toolbar.addAction(self.icon2)
        
        
        





        
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

    fenetre = vueClient()
    
    sys.exit(fenetre.app.exec())