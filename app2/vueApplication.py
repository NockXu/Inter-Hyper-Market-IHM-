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

        # Layouts
        self.layout_principal = QHBoxLayout()
        centre = QWidget()
        centre.setLayout(self.layout_principal)
        self.setCentralWidget(centre)

        self.menu_selection = QVBoxLayout()
        self.layout_principal.addLayout(self.menu_selection)

        self.liste_layout = QVBoxLayout()

        # Vues
        self.produitVue = VueProduit(self.controleur)
        self.planVue = VuePlan()
        self.planVue.hide()

        # Barre d'outils
        self.menu_bar = self.menuBar()
        fichier_menu = self.menu_bar.addMenu('Options')

        self.action_save = QAction('Enregistrer', self)
        fichier_menu.addAction(self.action_save)

        self.action_reset = QAction('Réinitialiser', self)
        fichier_menu.addAction(self.action_reset)

        # Widgets
        self.magasin = QPushButton("Choix magasin")
        self.magasin.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.magasin)

        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.liste_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.scroll_area)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.liste_layout.addItem(self.spacer)

        self.supp = QPushButton("Supprimer la liste")
        self.supp.setFont(QFont("Arial", 12))
        self.menu_selection.addWidget(self.supp)

        self.ajout_plan = QPushButton("Voir le plan")
        self.ajout_plan.setFixedHeight(self.height() // 8)
        self.ajout_plan.setFont(QFont("Arial", 15))
        self.menu_selection.addWidget(self.ajout_plan)
        
        self.layout_principal.addWidget(self.produitVue)
        self.layout_principal.addWidget(self.planVue)

        # Affichage
        self.setWindowTitle('Application client')
        self.showMaximized()

    def creer_produit_layout(self, nom_produit):
        layout = QHBoxLayout()
        label = QLabel(nom_produit)
        button = QPushButton("X")
        button.setFixedWidth(30)
        button.setFixedHeight(30)
        ligne_separation = QFrame()
        ligne_separation.setFrameShape(QFrame.Shape.HLine)
        ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
        
        button.clicked.connect(lambda: self.retirer_produit_liste(layout, ligne_separation))
        
        layout.addWidget(label)
        layout.addWidget(button)

        if self.liste_layout.count() > 1:
            self.liste_layout.insertWidget(self.liste_layout.count() - 1, ligne_separation)
        
        return layout

## Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VueApplication(app)
    sys.exit(app.exec())