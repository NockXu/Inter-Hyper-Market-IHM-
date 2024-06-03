import sys, os
from typing import List
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import vueDockMenuOutil
import vueDockMenuCarre
import vueDockProduit
from imageDeplacement import ImageDeplacement

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *

class MainWindow(QMainWindow):
    
    planCree = pyqtSignal(int, int, str, str, str, str, list)
    
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
        self.action_supprimer = QAction('Supprimer', self)
        menu_fichier.addAction(self.action_supprimer)

        # Menu Edition
        menu_edition = self.barre_menu.addMenu('Edition')
        self.action_reset = QAction('Réinitialiser', self)
        menu_edition.addAction(self.action_reset)

        # Menu Affichage
        menu_affichage = self.barre_menu.addMenu('Affichage')
        self.action_barre = QAction('Menu Outil', self)
        menu_affichage.addAction(self.action_barre)
        self.action_menu_graphe = QAction('Menu Graphe', self)
        menu_affichage.addAction(self.action_menu_graphe)

        self.plan_label = ImageDeplacement()

        #--------------------------------------------------------------------------------
        #                           Connexions des actions
        #--------------------------------------------------------------------------------

        self.action_barre.triggered.connect(self.basculer_menu_outil)
        self.action_reset.triggered.connect(self.reset_all)
        self.action_menu_graphe.triggered.connect(self.basculer_menu_graphe)
        
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

        self.dock3 = QDockWidget("Produits")
        self.vueProduit = vueDockProduit.VueDockProduit(self)
        self.dock3.setWidget(self.vueProduit)
        self.dock3.setFixedWidth(300)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock1)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock2)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock3)

        self.vueOutil.get_load_plan_button().clicked.connect(self.load_plan)
        
        self.vueCarre.carre_button.clicked.connect(self.create_grid)
        
        #--------------------------------------------------------------------------------
        #                           Paramètre menu Graphe
        #--------------------------------------------------------------------------------

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

    def load_plan(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger un plan", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(self.plan_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.plan_label.setPixmap(pixmap)
            self.plan_label.update_grid()

    def basculer_menu_outil(self):
        if self.dock1.isVisible():
            self.dock1.hide()
        else:
            self.dock1.show()

    def basculer_menu_graphe(self):
        if self.dock2.isVisible():
            self.dock2.hide()
        else:
            self.dock2.show()
    
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
        self.planCree.emit(rows, cols, nom, auteur, date, adresse, rects)
        
    def setRayonActuelle(self, nom: str, couleur: QColor) -> None:
        self.nomRayon = nom
        self.couleurRayon = couleur
        self.plan_label.set_brush_color(couleur)
    
    def updateCouleur(self, rects: dict[tuple[int, int], QColor]) -> None:
        self.plan_label.updateColor(rects)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
    with fichier_style:
        qss = fichier_style.read()
        app.setStyleSheet(qss)

    main = MainWindow()
    main.show()
    sys.exit(app.exec())
