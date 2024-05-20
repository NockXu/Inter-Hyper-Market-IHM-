import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox, QFileDialog, QSpacerItem
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
        
        # Layout de la liste de courses
        self.liste_layout = QVBoxLayout()
        
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
        self.magasin = QPushButton("Choix magasin")
        self.magasin.setFixedWidth(self.width() // 3)
        self.menu_selection.addWidget(self.magasin)

        # La liste de course
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
        self.magasin.clicked.connect(self.ouvrir_fichier)
        self.supp.clicked.connect(self.vider_liste)
        self.action_reset.triggered.connect(self.reset_application)


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
        # Layout du produit
        layout = QHBoxLayout()
        
        label = QLabel(nom_produit)
        button = QPushButton("X")
        button.setFixedWidth(30)
        button.setFixedHeight(30)
        
        button.clicked.connect(lambda: self.retirer_produit_liste(layout, ligne_separation))
        
        layout.addWidget(label)
        layout.addWidget(button)
        
        # Ligne separatrice
        ligne_separation = QFrame()
        ligne_separation.setFrameShape(QFrame.Shape.HLine)
        ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
        
        # Insert the product layout and separator before the spacer
        if self.liste_layout.count() > 1:  # Si il sagit du promier produit dans la liste, on n'ajoute pas de ligne separatrice
            # Ligne separatrice
            ligne_separation = QFrame()
            ligne_separation.setFrameShape(QFrame.Shape.HLine)
            ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
            self.liste_layout.insertWidget(self.liste_layout.count() - 1, ligne_separation)
        
        
        self.liste_layout.insertLayout(self.liste_layout.count() - 1, layout)
        
        
        print("produit ajouté : " + nom_produit)

        
    def retirer_produit_liste(self, layout, ligne_separation):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.liste_layout.removeItem(layout)
        layout.deleteLater()
        
        ligne_separation.setParent(None)
        
    # Fonction qui supprime la liste des produits
    def vider_liste(self):
        while self.liste_layout.count() > 1:
            item = self.liste_layout.itemAt(0)
            if isinstance(item, QHBoxLayout):
                self.retirer_produit_liste(item, item.itemAt(1).widget())
            elif isinstance(item.widget(), QFrame):
                item.widget().setParent(None)
            else:
                self.liste_layout.removeItem(item)
                item.widget().deleteLater()
        
    def ouvrir_fichier(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier", "", "All Files (*);;Text Files (*.txt)")
        if fileName:
            print("Fichier sélectionné:", fileName)
            self.vider_liste()
            self.produitVue.charger_produits(fileName)
            self.produitVue.filtre1.setCurrentIndex(0)
            self.produitVue.filtre2.setCurrentIndex(0)
            
            
    def reset_application(self):
        self.vider_liste()
        self.produitVue.reset_vue()
            
    

## Programme principal : test de la vue ---------------------------------------
if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VueApplication(app)
    sys.exit(app.exec())
