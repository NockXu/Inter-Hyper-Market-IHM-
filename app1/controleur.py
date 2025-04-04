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
        self.main_window.rectRayAttribuee.connect(self.setRay)
        
        self.main_window.imageAjouter.connect(self.main_window.set_plan)
        self.main_window.vueOutil.nomMagasinChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.nomProjetChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.addresseChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.dateChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.auteurChanger.connect(self.main_window.set_plan)
        self.main_window.vueOutil.loadPressed.connect(self.ouvrir_projet)

        self.main_window.plan_label.etagereAjoutee.connect(self.afficher_etageres)

        self.main_window.vueEtagere.etagereSelectionnee.connect(self.get_produits_etagere)

        self.main_window.vueProduit.produitAjoute.connect(self.creer_produit)
        self.main_window.vueEtagere.produitAjouteAvecEtagere.connect(self.ajouter_produit_etagere)

        self.main_window.vueEtagere.etagereSupprimee.connect(self.suprimer_etagere_model)

        self.main_window.show()

    def nouveau_projet(self):
        self.main_window.reset_all()
        self.model = Plan()

    def ouvrir_projet(self):
        file_path, _ = QFileDialog.getOpenFileName(self.main_window, "Ouvrir le fichier", "", "JSON Files (*.json)")
        if file_path:
            self.main_window.reset_all()
            self.model.lire_JSON(file_path)
            # le nom
            self.model.lire_JSON(file_path)
            self.main_window.vueOutil.nom_magasin.setText(self.model.get_nom())
            # l'auteur
            self.model.lire_JSON(file_path)
            self.main_window.vueOutil.auteur.setText(self.model.get_auteur())
            # l'addresse
            self.model.lire_JSON(file_path) 
            self.main_window.vueOutil.adresse.setText(self.model.get_adresse())
            # la date
            self.model.lire_JSON(file_path)
            date = QDate().fromString(self.model.get_date(), "dd/MM/yyyy")
            self.main_window.vueOutil.date.setDate(date)
            
            self.model.lire_JSON(file_path)
            # le nom du projet + image
            self.main_window.vueOutil.nom_projet.setText(self.model.get_fichier())
            self.main_window.vueOutil.image.lineEdit.setText(self.model.get_image())
            
            self.model.lire_JSON(file_path)
            # longeur et largeur
            self.main_window.vueCarre.nb_carre_x.set_valeur(self.model.get_h())
            self.main_window.vueCarre.nb_carre_y.set_valeur(self.model.get_l())
            
            if self.model.get_image():
                self.main_window.vueOutil.image.setImage(self.model.get_image())
            
            self.model.lire_JSON(file_path)
            infos = self.model.getInfos()
            self.main_window.vueCarre.tableRayon.set_data(infos)
            
            # la méthode suprime les données du modèle
            
            self.main_window.create_grid()
            # on le recrée
            self.model.lire_JSON(file_path)
            self.updateFonc()
            self.main_window.vueCarre.fonction.toggle_mode()
            self.model.lire_JSON(file_path)
            self.updateRayon()
            self.main_window.vueCarre.fonction.toggle_mode()
            self.updateEtagere()

    def enregistrer_projet(self):
        """Enregistre le projet en écrivant les données des rayons dans un fichier JSON."""
        self.model.ecrire_JSON(self.model.get_fichier())

    def setModele(self, rows: int, cols: int, nom: str, auteur: str, date: str, adresse: str, image: str) -> None:
        """Initialise le modèle avec les informations fournies."""
        self.model = Plan(rows, cols, nom, auteur, date, adresse, image)

    def creer_produit(self, nom_produit, categorie):
        """Crée un nouveau produit avec le nom et la catégorie spécifiés."""
        produit = Produit(nom_produit, 0.0, "", "", categorie)
        print("Produit créé :", produit)

    def creer_etagere(self, list_produits):
        """Crée une nouvelle étagère avec la liste de produits fournie."""
        etagere = Etagere(list_produits)
        print("L'étagère contient :", etagere)

    def ajouter_produit_etagere(self, produit, etagere):
        """Ajoute un produit spécifié à l'étagère spécifiée dans le modèle."""
        print(produit, etagere)
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if (x, y) == etagere:
                if produit:
                    produitm = Produit(produit, 0.0, "", "", "")
                    etagere: Etagere = point.get_fonction()
                    etagere.ajouter(produitm)
        print(produitm, etagere)

    def suprimer_etagere_model(self, nom_etagere: str):
        """Supprime l'étagère spécifiée du modèle."""
        nom_etagere = self.main_window.vueEtagere.nom_etagere_vers_tuple(nom_etagere)
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if nom_etagere[0] == x and nom_etagere[1] == y:
                point.set_fonction(Fonction())

    def set_etagere(self, rect: tuple, etagere) -> None:
        """Définit une étagère à la position spécifiée dans le modèle."""
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if rect[0] == x and rect[1] == y:
                point.set_fonction(Etagere(etagere))

    def set_produit_etagere(self, rect: tuple, produits):
        """Ajoute des produits à une étagère à la position spécifiée dans le modèle."""
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if rect[0] == x and rect[1] == y:
                if point.get_fonction().getNom() == 'etagere':
                    etagere: Etagere = point.get_fonction()
                    for produit in produits:
                        etagere.ajouter(produit)

    def updateEtagere(self) -> None:
        """Met à jour les données des étagères dans la vue."""
        rects: dict[tuple[int, int], list] = {}
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            produits: list = []
            etagere: Etagere = point.get_fonction()
            if isinstance(etagere, Etagere):
                for produit in etagere.get_produits():
                    if produit.get_nom():
                        produits.append(produit.get_nom())
                rects[(x, y)] = produits
        self.main_window.vueEtagere.set_data(rects)

    def updateRayon(self) -> None:
        """Met à jour les couleurs des rayons dans la vue."""
        rects: dict[tuple[int, int], QColor] = {}
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
        """Met à jour les fonctions des points dans la vue."""
        point: Point
        rects: dict[tuple[int, int], str] = {}
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

    def setCouleurRayon(self, name: str, color: QColor, newColor: QColor) -> None:
        """Définit une nouvelle couleur pour un rayon spécifié."""
        self.model.set_rayon(name, color, newColor)
        self.updateRayon()

    def delRayon(self, name: str, color: QColor):
        """Supprime un rayon spécifié du modèle."""
        self.model.del_rayon(name, color)
        self.main_window.nomRayon = None
        self.main_window.couleurRayon = QColor("white")
        self.main_window.couleurRayon.setAlpha(0)
        self.main_window.plan_label.set_brush_color(QColor("white"))
        self.updateRayon()

    def rectColorier(self, rect) -> None:
        """Colore un rectangle spécifié dans le modèle."""
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == rect[0] and y == rect[1]:
                point.setRayon(Rayon(self.main_window.nomRayon, self.main_window.couleurRayon))

    def setFonc(self, rect: tuple, name: str, color: QColor) -> None:
        """Définit une fonction pour un point à la position spécifiée dans le modèle."""
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == rect[0] and y == rect[1]:
                if name == 'etagere':
                    point.set_fonction(Etagere())
                elif name == 'chemin':
                    point.set_fonction(Chemin())
                elif name == 'entree':
                    point.set_fonction(Entree())

    def setRay(self, rect: tuple, name: str, color: QColor) -> None:
        """Définit un rayon pour un point à la position spécifiée dans le modèle."""
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == rect[0] and y == rect[1]:
                if name:
                    if color:
                        point.setRayon(Rayon(name, color))

    def delFonc(self, rect: tuple) -> None:
        """Supprime la fonction d'un point à la position spécifiée dans le modèle."""
        point: Point
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            if x == rect[0] and y == rect[1]:
                point.set_fonction(Fonction())

    def afficher_etageres(self, coords):
        """Affiche les coordonnées des étagères spécifiées."""
        print("Coordonnées des étagères :", coords)

    def get_produits_etagere(self) -> dict[tuple[int, int], dict]:
        """Récupère les produits de chaque étagère dans le modèle."""
        dico = {}
        for point in self.model.get_plan():
            x = point.get_x()
            y = point.get_y()
            etagere = point.get_fonction()
            if isinstance(etagere, Etagere):
                co = (x, y)
                dico[co] = {'nom': f'Etagere_{x}_{y}', 'produits': []}
                produits = etagere.get_produits()
                if produits:
                    for produit in produits:
                        dico[co]['produits'].append({'nom': produit.get_nom()})
        return dico

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