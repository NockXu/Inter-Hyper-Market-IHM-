import sys
import vueDockMenuOutil
import vueDockMenuCarre
import imageDeplacement
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.app = QApplication(sys.argv)
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.app.setStyleSheet(qss)

        # Barre de menus
        self.menu_bar = self.menuBar()

        # Menu Fichier
        file_menu = self.menu_bar.addMenu('Fichier')
        self.action_nouveau = QAction('Nouveau', self)
        file_menu.addAction(self.action_nouveau)

        self.action_ouvrir = QAction('Ouvrir', self)
        file_menu.addAction(self.action_ouvrir)

        self.action_enregistrer = QAction('Enregistrer', self)
        file_menu.addAction(self.action_enregistrer)

        self.action_supprimer = QAction('Supprimer', self)
        file_menu.addAction(self.action_supprimer)

        # Menu Edition
        edit_menu = self.menu_bar.addMenu('Edition')
        self.action_reset = QAction('Réinitialiser', self)
        edit_menu.addAction(self.action_reset)

        # Menu Affichage
        view_menu = self.menu_bar.addMenu('Affichage')
        self.action_barre = QAction('Menu Outil', self)
        view_menu.addAction(self.action_barre)
        
        self.action_menu_graphe = QAction('Menu Graphe', self)
        view_menu.addAction(self.action_menu_graphe)
        
        

        # Connecter l'action 'Menu' à la méthode toggle_menu_outil
        self.action_barre.triggered.connect(self.toggle_menu_outil)

        # Utiliser QScrollArea pour l'image
        self.scroll_area = QScrollArea()
        self.plan_label = imageDeplacement.ImageDeplacement()
        self.scroll_area.setWidget(self.plan_label)
        self.scroll_area.setWidgetResizable(True)

        self.layout_right = QVBoxLayout()
        self.layout_right.addWidget(self.scroll_area)

        #--------------------------------------------------------------------------------

        self.layout_groupe = QHBoxLayout()
        self.layout_groupe.addLayout(self.layout_right)

        self.widget_centre = QWidget()
        self.widget_centre.setLayout(self.layout_groupe)
        self.setCentralWidget(self.widget_centre)

        #--------------------------------------------------------------------------------

        self.dock1 = QDockWidget("Menu Outil")
        self.vueOutil : vueDockMenuOutil = vueDockMenuOutil.VueDockMenuOutil(self)
        self.dock1.setWidget(self.vueOutil)
        self.dock1.setFixedWidth(300)
        
        self.dock2 = QDockWidget("Menu Graphe")
        self.vueCarre : vueDockMenuCarre = vueDockMenuCarre.VueDockMenuCarre(self)
        self.dock2.setWidget(self.vueCarre)
        self.dock2.setFixedWidth(300)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock1)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock2)

        # Connecter le bouton load_plan_button à la méthode load_plan
        self.vueOutil.get_load_plan_button().clicked.connect(self.load_plan)

        #--------------------------------------------------------------------------------

        # Paramètres d'affichage
        self.setWindowTitle('INTER-HYPER-MARKET')
        self.showMaximized()
        self.polygon = QPolygon()
        self.show()

    def load_plan(self):
        # Ouvre une boîte de dialogue pour sélectionner une image
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger un plan", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_name:
            # Affiche l'image sélectionnée dans le QLabel du layout droit
            pixmap = QPixmap(file_name)
            self.plan_label.setPixmap(pixmap)
            self.plan_label.adjustSize()
            self.plan_label.updatePolygon()

    def toggle_menu_outil(self):
        if self.dock1.isVisible():
            self.dock1.hide()
        else:
            self.dock1.show()
            
    def toggle_menu_graphe(self):
        if self.dock2.isVisible():
            self.dock2.hide()
        else:
            self.dock2.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
