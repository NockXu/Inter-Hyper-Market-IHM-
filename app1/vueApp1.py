import sys, os
import vueDockMenuOutil
import vueDockMenuCarre
import imageDeplacement
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app = QApplication(sys.argv)
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.app.setStyleSheet(qss)

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

        #--------------------------------------------------------------------------------
        #                           Connexions des actions
        #--------------------------------------------------------------------------------

        self.action_barre.triggered.connect(self.basculer_menu_outil)
        self.action_reset.triggered.connect(self.reset_all)
        self.action_menu_graphe.triggered.connect(self.basculer_menu_graphe)

        #--------------------------------------------------------------------------------
        #                           Zone de l'image déplaçable
        #--------------------------------------------------------------------------------

        self.scroll_area = QScrollArea()
        self.plan_label = imageDeplacement.ImageDeplacement()
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

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock1)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock2)

        self.vueOutil.get_load_plan_button().clicked.connect(self.load_plan)
        self.vueCarre.carre_button.clicked.connect(self.create_grid)

        #--------------------------------------------------------------------------------
        #                           Paramètres d'affichage
        #--------------------------------------------------------------------------------

        self.setWindowTitle('INTER-HYPER-MARKET')
        self.showMaximized()
        self.polygon = QPolygon()
        self.show()

    #------------------------------------------------------------------------------------
    #                           Méthodes de classe
    #------------------------------------------------------------------------------------

    def load_plan(self):
        # Ouvre une interface pour sélectionner une image
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger un plan", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_name:
            # Affiche l'image sélectionnée dans le QLabel du layout droit
            pixmap = QPixmap(file_name)
            self.plan_label.setPixmap(pixmap)
            self.plan_label.adjustSize()
            self.plan_label.updatePolygon()

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
        rows = int(self.vueCarre.nb_carre_x.text())
        cols = int(self.vueCarre.nb_carre_y.text())
        if self.plan_label.pixmap() and rows > 0 and cols > 0:
            pixmap_rect = self.plan_label.getPixmapRect()
            pixmap_width = pixmap_rect.width()
            pixmap_height = pixmap_rect.height()
            cell_width = pixmap_width / cols
            cell_height = pixmap_height / rows

            polygons = []
            for row in range(rows):
                for col in range(cols):
                    top_left = QPointF(pixmap_rect.topLeft()) + QPointF(col * cell_width, row * cell_height)
                    top_right = top_left + QPointF(cell_width, 0)
                    bottom_right = top_left + QPointF(cell_width, cell_height)
                    bottom_left = top_left + QPointF(0, cell_height)
                    polygon = QPolygonF([top_left, top_right, bottom_right, bottom_left])
                    polygons.append(polygon)

            self.plan_label.set_polygons(polygons)
            self.plan_label.update()

#----------------------------------------------------------------------------------------
#                           Main
#----------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
