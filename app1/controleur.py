# controller.py
import json
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
        # Récupérez les données des rayons depuis le modèle
        data = self.get_rayons_data()

        # Sauvegardez les données dans un fichier JSON
        file_path, _ = QFileDialog.getSaveFileName(self.main_window, "Enregistrer le fichier", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

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

    def get_rayons_data(self):
        data = []
        
        # Add "info_plan" section
        info_plan = {
            "info_plan": {
                "nom": self.model._nom,
                "auteur": self.model._auteur,
                "adresse": self.model._adresse,
                "date": self.model._date
            }
        }
        data.append(info_plan)

        # Add rayons data
        for point in self.model.get_plan():
            rayon = {
                "x": point.get_x(),
                "y": point.get_y(),
                "voisins": [], 
                "fonction": {
                    "spécialitée": "étagère",
                    "acces": [True, True, True, True],
                    "produits": []
                },
                "rectangle": "None",
                "rayon": {
                    "nom": point.getRayon().getNom(),
                }
            }
            data.append(rayon)
        
        return data


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