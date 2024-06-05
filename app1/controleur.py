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
        
        
        self.main_window.planCree.connect(self.setModele)
        self.main_window.rectFoncAttribuee.connect(self.setFonc)
        self.main_window.plan_label.rectFoncSupprimee.connect(self.delFonc)
        
        # Signaux de TableWidget
        self.main_window.vueCarre.tableRayon.rayonRetire.connect(self.delRayon)
        #self.main_window.vueCarre.tableRayon.nomRayonChangee.connect()
        self.main_window.vueCarre.tableRayon.couleurRayonChangee.connect(self.setCouleurRayon)
        
        # Signaux de imageDeplacement
        self.main_window.plan_label.rectColoriee.connect(self.rectColorier)
        
        self.main_window.imageAjouter.connect(self.main_window.set_plan)
        self.main_window.vueOutil.nomMagasinChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.nomProjetChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.addresseChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.dateChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.auteurChanger.connect(self.main_window.set_plan)

        self.main_window.show()

    def nouveau_projet(self):
        self.main_window.reset_all()
        self.model = Plan()

    def ouvrir_projet(self):
        file_path, _ = QFileDialog.getOpenFileName(self.main_window, "Ouvrir le fichier", "", "JSON Files (*.json)")
        if file_path:
            self.model.lire_JSON(file_path)
            # le nom
            self.main_window.vueOutil.nom_magasin.setText(self.model.get_nom())
            # l'auteur
            self.main_window.vueOutil.auteur.setText(self.model.get_auteur())
            # l'addresse
            self.main_window.vueOutil.adresse.setText(self.model.get_adresse())
            # la date
            date = QDate().fromString(self.model.get_date(), "dd/MM/yyyy")
            self.main_window.vueOutil.date.setDate(date)
            # le nom du projet + image
            self.main_window.vueOutil.nom_projet.setText(self.model.get_fichier())
            self.main_window.vueOutil.image.lineEdit.setText(self.model.get_image())
            # longeur et largeur
            self.main_window.vueCarre.nb_carre_x.set_valeur(self.model.get_h())
            self.main_window.vueCarre.nb_carre_y.set_valeur(self.model.get_l())
            
            if self.model.get_image():
                self.main_window.vueOutil.image.setImage(self.model.get_image())
            
            infos = self.model.getInfos()
            self.main_window.vueCarre.tableRayon.set_data(infos)
            
            # la méthode suprime les données du modèle
            self.main_window.create_grid()
            # on le recrée
            self.model.lire_JSON(file_path)
            self.updateFonc()
            self.main_window.vueCarre.fonction.toggle_mode()
            self.updateRayon()

    def enregistrer_projet(self):
        # Récupérez les données des rayons depuis le modèle
        self.model.ecrire_JSON(self.model.get_fichier())

    def setModele(self, rows : int, cols : int, nom : str, auteur : str, date : str, adresse : str, image : str) -> None:
        self.model = Plan(rows, cols, nom, auteur, date, adresse, image)
    
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
        
    def updateFonc(self) -> None:
        point : Point
        rects : dict[tuple[int, int], QColor] = {}
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            nom = point.get_fonction().getNom()
            if nom:
                rects[(x, y)] = nom
            else:
                rects[(x, y)] = None
            nom = None
        self.main_window.plan_label.updateFonc(rects)
        
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
        
    def rectColorier(self, rect) -> None:
        point : Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == rect[0] and y == rect[1]:
                point.setRayon(Rayon(self.main_window.nomRayon, self.main_window.couleurRayon))
                
    def setFonc(self, rect : tuple, name : str, color : QColor) -> None:
        point : Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == rect[0] and y == rect[1]:
                point.set_fonction(Fonction(name, color))
                
    def delFonc(self, rect : tuple) -> None:
        point : Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == rect[0] and y == rect[1]:
                point.set_fonction(Fonction())

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