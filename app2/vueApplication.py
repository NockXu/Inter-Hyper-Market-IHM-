import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont
from vueProduit import *


##########################################################
#                                                        #
#                 Classe vueApplication                  #
#                                                        #
##########################################################
class VueApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.app.setStyleSheet(qss)
        self.setupUI()

    def setupUI(self):
        self.layout_principal = QHBoxLayout()
        centre = QWidget()
        centre.setLayout(self.layout_principal)
        self.setCentralWidget(centre)

        self.menu_selection = QVBoxLayout()
        self.layout_principal.addLayout(self.menu_selection)

        self.toolbar = QToolBar('')
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        self.action_save = QAction('Enregistrer', self)
        self.toolbar.addAction(self.action_save)

        self.toolbar.addSeparator() 
        self.icon2 = QAction('Réinitialiser', self)
        self.toolbar.addAction(self.icon2)

        self.magasin = QComboBox()
        self.magasin.addItem("Choix du magasin")
        self.magasin.addItem("Magasin 1")
        self.magasin.addItem("Magasin 2")
        self.magasin.addItem("Magasin 3")
        self.magasin.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.magasin)

        self.liste = QTextEdit()
        self.liste.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.liste)
        
        self.ajout_plan = QPushButton("Voir le plan")
        self.ajout_plan.setFixedHeight(self.height() // 8)
        self.ajout_plan.setFont(QFont("Arial", 15))
        self.menu_selection.addWidget(self.ajout_plan)

        # Appel de la fonction setup_vue_produit depuis le module vueProduit
        vue_produit(self.layout_principal)


        self.show()
        
if __name__ == "__main__":
    print(f' --- main --- ')
    fenetre = VueApplication()
    fenetre.setWindowTitle('Application client')
    fenetre.showMaximized()
    sys.exit(fenetre.app.exec())
