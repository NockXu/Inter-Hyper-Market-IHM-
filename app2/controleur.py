import sys, os
from PyQt6.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QFrame, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from vueApplication import VueApplication

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *

class Controleur:
    
    chemin_trouve = pyqtSignal(list)
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.vue_application = VueApplication(self)
        self.panier = [] #Produits de la liste de course du client
        self.connect_signals()
        self.plan = Plan()
        self.vue_application.show()
        sys.exit(self.app.exec())

    # Fonction d'appel des signaux
    def connect_signals(self):
        self.vue_application.ajout_plan.clicked.connect(self.changer_vue)
        self.vue_application.produit_ajoute.connect(self.ajouter_produit_liste)
        self.vue_application.magasin.clicked.connect(self.ouvrir_fichier)
        self.vue_application.supp.clicked.connect(self.vider_liste)
        self.vue_application.action_reset.triggered.connect(self.reset_application)
        self.vue_application.ouvrir.triggered.connect(self.ouvrir_fichier)
        
     # Fonction qui permet de changer de vu entre les produits du magasin et le plan 
    def changer_vue(self):
        if self.vue_application.produitVue.isVisible():
            self.vue_application.produitVue.hide()
            self.vue_application.ajout_plan.setText("Ajouter des produits")
            self.trouver_chemin() # Appel de la fonction permettant de trouver le chemin le plus court
            self.vue_application.planVue.show()
        else:
            self.vue_application.produitVue.show()
            self.vue_application.planVue.hide()
            self.vue_application.planVue.supprimer_chemin() # Supprime le chemin pour evité une superposition des chemins
            self.vue_application.ajout_plan.setText("Voir le plan")
            

    # Fonction qui permet de trouver le chemin le plus rapide vers les produits du panier    
    def trouver_chemin(self):
        points = self.plan.get_plan()
        depart_point = None

        # Trouver le point de départ avec la spécialité "entree"
        for point in points:
            if isinstance(point.get_fonction(), Entree): # Si l'instance Entree est trouver alors il sagit de l'entree du magasin
                depart_point = point
                break

        point_article = [] # Liste des coordonnées des articles

        for nom_produit in self.panier:
            arrivee_point = None
            for point in points:
                if isinstance(point.get_fonction(), Etagere):
                    etagere = point.get_fonction()
                    if any(produit.get_nom() == nom_produit for produit in etagere.get_produits()):
                        arrivee_point = point
                        break
            
            if arrivee_point and arrivee_point not in point_article: # Ajoute à la liste si le point n'y est pas deja 
                point_article.append(arrivee_point)
        
        chemin = self.plan.chemin_rapide(depart_point, point_article) # Appel de la fonction de recherche du chemin dans le dossier Classes et le fichier plan
        self.vue_application.planVue.afficher_chemin(chemin, self.plan.get_l(), self.plan.get_h()) # Appel de la fonction avec le nombre de lignes et de colones
        print(chemin)



    # Fonction qui ajoute les produits sélectionners à la liste et les affiches dans un layout à part
    def ajouter_produit_liste(self, nom_produit):
        if nom_produit in self.panier:
            print("Le produit", nom_produit, "est déjà dans le panier.")
            return

        self.panier.append(nom_produit)
        layout = QHBoxLayout()
        
        label = QLabel(nom_produit)
        button = QPushButton()
        button.setIcon(QIcon('app2/image/poubelle.png'))
        button.setFixedWidth(30)
        button.setFixedHeight(30)
        
        ligne_separation = QFrame()
        ligne_separation.setFrameShape(QFrame.Shape.HLine)
        ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
        
        # Permet de supprimer un arcticle de la liste en appuyant sur le bouton poubelle
        button.clicked.connect(lambda: self.retirer_produit_liste(layout, ligne_separation))
        
        layout.addWidget(label)
        layout.addWidget(button)
        
        if self.vue_application.liste_layout.count() > 1:  # Si il s'agit du premier produit dans la liste, on n'ajoute pas de ligne séparatrice
            self.vue_application.liste_layout.insertWidget(self.vue_application.liste_layout.count() - 1, ligne_separation)
        
        self.vue_application.liste_layout.insertLayout(self.vue_application.liste_layout.count() - 1, layout)
        
        print("produit ajouté : " + nom_produit)


    # Fonction de suppression d'un produit de la liste 
    def retirer_produit_liste(self, layout, ligne_separation):
        
        # Récuperation du nom du produit dans le label pour supprimer le produit du panier
        label = layout.itemAt(0).widget()
        if isinstance(label, QLabel):
            nom_produit = label.text()
            if nom_produit in self.panier:
                self.panier.remove(nom_produit)
                print("Produit retiré : " + nom_produit)
        
        # Utilisation de reversed() pour acceder à la liste de layout dans l'autre sens
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.vue_application.liste_layout.removeItem(layout) # Sppression du layout que l'on souhaite supprimer
        layout.deleteLater()
        
        ligne_separation.setParent(None)
     

    # Fonction qui permet de vider entièrement la liste des produits du panier 
    def vider_liste(self):        
        while self.vue_application.liste_layout.count() > 1:
            item = self.vue_application.liste_layout.itemAt(0)
            if isinstance(item.layout(), QHBoxLayout):
                for i in reversed(range(item.layout().count())):
                    widget = item.layout().itemAt(i).widget()
                    if widget:
                        widget.setParent(None)
                self.vue_application.liste_layout.removeItem(item.layout())
                item.layout().deleteLater()
            elif isinstance(item.widget(), QFrame):
                item.widget().setParent(None)
            else:
                self.vue_application.liste_layout.removeItem(item)
                item.widget().deleteLater()
        
        self.panier.clear()

    # Fonction d'ouverture du fichier json 
    def ouvrir_fichier(self):
        fileName, _ = QFileDialog.getOpenFileName(self.vue_application, "Ouvrir le fichier", "", "JSON Files (*.json);;All Files (*)")
        print(fileName)
        if fileName:
            self.vider_liste()
            self.plan.lire_JSON(fileName)
            self.vue_application.produitVue.charger_produits(self.plan.get_plan()) # Affichage des produits du magasin
            self.vue_application.produitVue.filtre1.setCurrentIndex(0) #Sélection des filtre remis à 0
            self.vue_application.planVue.supprimer_plan() # Supprime un plan si il en existe deja un
            self.vue_application.planVue.afficher_plan(self.plan.get_image()) # Affichage du nouveau plan

    # Remise à zero de l'application 
    def reset_application(self):
        self.vue_application.produitVue.reset_vue() # Supprime les produits afficher sur la page
        self.vider_liste() # Supprime le panier en entier
        self.vue_application.planVue.supprimer_plan() # Supprime le plan
        self.vue_application.produitVue.reset_vue() #réinitialise l'affichage des produits
        self.vue_application.planVue.supprimer_chemin() # Supprime le chemin 


if __name__ == "__main__":
    controleur = Controleur()
    