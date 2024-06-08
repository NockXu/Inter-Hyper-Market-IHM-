import sys, os
from typing import List
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from TableWidget import TableWidget
import vueDockMenuOutil
import vueDockMenuCarre
import vueDockProduit
import vueDockEtagere
from imageDeplacement import ImageDeplacement

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *

class MainWindow(QMainWindow):
    
    # Signaux
    planCree = pyqtSignal(int, int, str, str, str, str, str)
    rectFoncAttribuee = pyqtSignal(tuple, str, QColor)
    rectRayAttribuee = pyqtSignal(tuple, str, QColor)
    imageAjouter = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

        #--------------------------------------------------------------------------------
        #                           Barre de menus
        #--------------------------------------------------------------------------------

        self.barre_menu = self.menuBar()

        # Menu Fichier
        menu_fichier = self.barre_menu.addMenu('Fichier')
        self.action_nouveau = QAction('Nouveau', self)
        menu_fichier.addAction(self.action_nouveau)
        self.action_ouvrir = QAction('Ouvrir', self)
        menu_fichier.addAction(self.action_ouvrir)
        self.action_enregistrer = QAction('Enregistrer', self)
        menu_fichier.addAction(self.action_enregistrer)

        # Menu Edition
        menu_edition = self.barre_menu.addMenu('Edition')
        self.action_reset = QAction('Réinitialiser', self)
        menu_edition.addAction(self.action_reset)

        # Menu Affichage
        menu_affichage = self.barre_menu.addMenu('Affichage')

        self.plan_label = ImageDeplacement()

        #--------------------------------------------------------------------------------
        #                           Connexions des actions
        #--------------------------------------------------------------------------------

        self.action_reset.triggered.connect(self.reset_all)
        
        #--------------------------------------------------------------------------------
        #                           Slots controleur
        #--------------------------------------------------------------------------------

        self.plan_label.getRectsDeclenchee.connect(self.set_plan)

        #--------------------------------------------------------------------------------
        #                           Zone de l'image déplaçable
        #--------------------------------------------------------------------------------

        self.scroll_area = QScrollArea()
        
        self.scroll_area.setWidget(self.plan_label)
        self.scroll_area.setWidgetResizable(True)

        self.layout_right = QVBoxLayout()
        self.layout_right.addWidget(self.scroll_area)

        #--------------------------------------------------------------------------------
        #                           Layout principal
        #--------------------------------------------------------------------------------

        self.layout_groupe = QHBoxLayout()
        self.layout_groupe.addLayout(self.layout_right)

        self.widget_centre = QWidget()
        self.widget_centre.setLayout(self.layout_groupe)
        self.setCentralWidget(self.widget_centre)

        #--------------------------------------------------------------------------------
        #                           Dock Widgets
        #--------------------------------------------------------------------------------

        self.dock1 = QDockWidget("Menu Outil")
        self.vueOutil = vueDockMenuOutil.VueDockMenuOutil(self)
        self.dock1.setWidget(self.vueOutil)
        self.dock1.setFixedWidth(300)
        
        self.dock2 = QDockWidget("Menu Graphe")
        self.vueCarre = vueDockMenuCarre.VueDockMenuCarre(self)
        self.dock2.setWidget(self.vueCarre)
        self.dock2.setFixedWidth(300)
        self.dock2.setMaximumHeight(700)

        self.dock3 = QDockWidget("Produits")
        table_widget = TableWidget()
        self.vueProduit = vueDockProduit.VueDockProduit(table_widget)
        self.dock3.setWidget(self.vueProduit)
        self.dock3.setFixedWidth(300)

        self.dock4 = QDockWidget("Menu Etagere")
        self.vueEtagere = vueDockEtagere.VueEtagere()
        self.dock4.setWidget(self.vueEtagere)
        self.dock4.setFixedWidth(300)
        self.dock4.setMaximumHeight(400)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock1)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock2)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock3)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock4)

        menu_affichage.addAction(self.dock1.toggleViewAction())
        menu_affichage.addAction(self.dock2.toggleViewAction())
        menu_affichage.addAction(self.dock3.toggleViewAction())
        menu_affichage.addAction(self.dock4.toggleViewAction())

        self.vueOutil.image.imageSelectionnee.connect(self.load_plan)

        self.vueCarre.carre_button.clicked.connect(self.create_grid)
        
        #--------------------------------------------------------------------------------
        #                           Paramètre menu Graphe
        #--------------------------------------------------------------------------------

        # fonctionRect
        self.nomFonction = None
        self.couleurFonction = None
        # Signaux
        self.vueCarre.fonction.fonctionSelectionnee.connect(self.setFonctionActuelle)
        self.vueCarre.fonction.bouton_chemin.couleurChangee.connect(self.plan_label.setChemin)
        self.vueCarre.fonction.bouton_entree.couleurChangee.connect(self.plan_label.setEntree)
        self.vueCarre.fonction.bouton_etagere.couleurChangee.connect(self.plan_label.setEtagere)
        self.vueCarre.fonction.boutonCliquee.connect(self.plan_label.set_fonction_actuelle)
        self.vueCarre.fonction.modeChangee.connect(self.plan_label.switch_est_fonction)
        self.plan_label.rectFoncAttribuee.connect(self.getRectFonc)
        self.plan_label.rectColoriee.connect(self.getRectRay)
        self.plan_label.etagereAjoutee.connect(self.vueEtagere.ajouterEtagere)
        
    
        # TableWidget
        self.nomRayon = None
        self.couleurRayon = None
        # signaux
        self.vueCarre.tableRayon.rayonSelectionee.connect(self.setRayonActuelle)

        #--------------------------------------------------------------------------------
        #                           Paramètres d'affichage
        #--------------------------------------------------------------------------------

        self.setWindowTitle('INTER-HYPER-MARKET')
        self.showMaximized()
        self.show()

    #------------------------------------------------------------------------------------
    #                           Méthodes de classe
    #------------------------------------------------------------------------------------

    def load_plan(self, file_name : str):
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(self.plan_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.plan_label.setPixmap(pixmap)
            self.plan_label.update_grid()
            self.imageAjouter.emit(file_name)
    
    def reset_all(self):
        self.plan_label.clear()
        self.plan_label.clearAll()
        self.plan_label.update()
        self.vueCarre.reset()
        self.vueOutil.reset()

    def create_grid(self):
        rows = int(self.vueCarre.nb_carre_x.valeur)
        cols = int(self.vueCarre.nb_carre_y.valeur)
        if rows > 0 and cols > 0:
            self.plan_label.set_grid(rows, cols)

    def set_plan(self, rects: List[QRectF]):
        rows = int(self.vueCarre.nb_carre_x.valeur)
        cols = int(self.vueCarre.nb_carre_y.valeur)
        nom = self.vueOutil.nom_magasin.text()
        auteur = self.vueOutil.auteur.text()
        date = self.vueOutil.date.text()
        adresse = self.vueOutil.adresse.text()
        image = self.vueOutil.image.lineEdit.text()
        self.planCree.emit(rows, cols, nom, auteur, date, adresse, image)
        
    def setRayonActuelle(self, nom: str, couleur: QColor) -> None:
        if self.vueCarre.fonction.mode_fonction:
            self.vueCarre.fonction.bouton_fonction.click()
        self.nomRayon = nom
        self.couleurRayon = couleur
        self.couleurRayon.setAlpha(128)
        self.plan_label.set_brush_color(couleur)
    
    def updateCouleur(self, rects: dict[tuple[int, int], QColor]) -> None:
        self.plan_label.updateColor(rects)
        
    def setFonctionActuelle(self, name :str = None, color : QColor = None) -> None:
        if self.vueCarre.fonction.chemin_active:
            self.nomFonction = name
            self.couleurFonction = color
        
        elif self.vueCarre.fonction.entree_active:
            self.nomFonction = name
            self.couleurFonction = color
            
        elif self.vueCarre.fonction.etagere_active:
            self.nomFonction = name
            self.couleurFonction = color
        
        else:
            self.nomFonction = None
            self.couleurFonction = None
    
    def getRectFonc(self, rect : tuple) -> None:
        if self.nomFonction and self.couleurFonction:
            self.rectFoncAttribuee.emit(rect, self.nomFonction, self.couleurFonction)
            
    def getRectRay(self, rect : tuple) -> None:
        if self.nomRayon and self.couleurRayon:
            self.rectRayAttribuee.emit(rect, self.nomRayon, self.couleurRayon)
            

if __name__ == "__main__":

    app = QApplication(sys.argv)
    fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
    with fichier_style:
        qss = fichier_style.read()
        app.setStyleSheet(qss)

    main = MainWindow()
    main.show()
    sys.exit(app.exec())
