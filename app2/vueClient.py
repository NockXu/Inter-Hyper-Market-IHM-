import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont

##########################################################
#                                                        #
#                    Classe vueClient                    #
#                                                        #
##########################################################
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

        # Layouts des filtres 
        self.filtre1_layout = QVBoxLayout()
        self.layout_principal.addLayout(self.filtre1_layout)
        self.filtre2_layout = QHBoxLayout()
        
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

        
        # Filtre
        self.filtre_label = QLabel("Filtre")
        self.filtre1_layout.addWidget(self.filtre_label)

        # Filtre du type de produit
        self.filtre1 = QComboBox()
        self.filtre1.addItem("Type de produit")
        self.filtre1.addItem("Option 2")
        self.filtre1.setFixedWidth(self.width() // 4)  # Définit la largeur du menu déroulant à 1/4 de la largeur de la fenêtre
        self.filtre2_layout.addWidget(self.filtre1)

        # Filtre du rayon
        self.filtre2 = QComboBox()
        self.filtre2.addItem("Rayon")
        self.filtre2.addItem("Option B")
        self.filtre2.setFixedWidth(self.width() // 4)
        self.filtre2_layout.addWidget(self.filtre2)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) #Permet de modifier l'espace créer pour que l'icone soit à droite
        self.toolbar.addWidget(spacer)
        self.filtre_label1 = QLabel(" ")
        self.filtre2_layout.addWidget(self.filtre_label1)
        self.filtre1_layout.addLayout(self.filtre2_layout)
        
        image_label = QLabel(self)
        pixmap = QPixmap("image/plan1.jpg")
        image_label.setPixmap(pixmap)
        self.filtre1_layout.addWidget(image_label)







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