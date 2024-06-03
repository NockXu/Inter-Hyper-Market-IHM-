# controller.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from vueApp1 import MainWindow
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *

class Controleur:
    def __init__(self):
        self.main_window = MainWindow()
        self.model = Plan() 

        # Connexion des signaux
        self.main_window.action_nouveau.triggered.connect(self.nouveau_projet)
        self.main_window.action_ouvrir.triggered.connect(self.ouvrir_projet)
        self.main_window.action_enregistrer.triggered.connect(self.enregistrer_projet)
        self.main_window.action_supprimer.triggered.connect(self.supprimer_projet)
        self.main_window.action_reset.triggered.connect(self.reset_all)
        self.main_window.action_barre.triggered.connect(self.basculer_menu_outil)
        self.main_window.action_menu_graphe.triggered.connect(self.basculer_menu_graphe)
        self.main_window.planCree.connect(self.setModele)
        
        # Signaux de TableWidget
        self.main_window.vueCarre.tableRayon.rayonRetire.connect(self.delRayon)
        #self.main_window.vueCarre.tableRayon.nomRayonChangee.connect()
        self.main_window.vueCarre.tableRayon.couleurRayonChangee.connect(self.setCouleurRayon)
        
        # Signaux de imageDeplacement
        self.main_window.plan_label.rectColoriee.connect(self.rectColorier)

        self.main_window.show()

    def nouveau_projet(self):
        # Implémentez la logique pour créer un nouveau projet
        pass

    def ouvrir_projet(self):
        # Implémentez la logique pour ouvrir un projet existant
        pass

    def enregistrer_projet(self):
        # Implémentez la logique pour enregistrer le projet
        pass

    def supprimer_projet(self):
        # Implémentez la logique pour supprimer le projet
        pass

    def reset_all(self):
        # Réinitialiser tous les paramètres
        pass

    def basculer_menu_outil(self):
        # Afficher ou masquer le menu outil
        pass

    def basculer_menu_graphe(self):
        # Afficher ou masquer le menu graphe
        pass

    def setModele(self, rows : int, cols : int, nom : str, auteur : str, date : str, adresse : str, rects : list[QRectF]) -> None:
        self.model = Plan(rows, cols, nom, auteur, date, adresse)
        self.model.lienQPlan(rects)
    
    def updateRayon(self) -> None:
        rects : dict[tuple[int, int], QColor] = {}
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            couleur = point.getRayon().getCouleur()
            if couleur:
                rects[(x, y)] = couleur
            else:
                rects[(x, y)] = QColor("white")
                rects[(x, y)].setAlpha(0)
            couleur = None
        self.main_window.plan_label.updateColor(rects)
        
    def setCouleurRayon(self, name : str, color : QColor, newColor : QColor) -> None:
        
        self.model.set_rayon(name, color, newColor)
        self.updateRayon()    
    
    def delRayon(self, name : str, color : QColor):
        self.model.del_rayon(name, color)
        self.main_window.nomRayon = None
        self.main_window.couleurRayon = QColor("white")
        self.main_window.couleurRayon.setAlpha(0)
        self.main_window.plan_label.set_brush_color(QColor("white"))
        self.updateRayon()
        
    def rectColorier(self, xy) -> None:
        point : Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == xy[0] and y == xy[1]:
                point.setRayon(Rayon(self.main_window.nomRayon, self.main_window.couleurRayon))


# Programme principal : test du controleur ------------------------------------
if __name__ == "__main__" :

    print('TEST: class Controleur')
    
    app = QApplication(sys.argv)
    fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
    with fichier_style:
        qss = fichier_style.read()
        app.setStyleSheet(qss)
    
    control = Controleur()
    
    sys.exit(app.exec())