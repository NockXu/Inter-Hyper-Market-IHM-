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

    def connect_signals(self):
        self.vue_application.ajout_plan.clicked.connect(self.changer_vue)
        self.vue_application.produit_ajoute.connect(self.ajouter_produit_liste)
        self.vue_application.magasin.clicked.connect(self.ouvrir_fichier)
        self.vue_application.supp.clicked.connect(self.vider_liste)
        self.vue_application.action_reset.triggered.connect(self.reset_application)
        self.vue_application.ouvrir.triggered.connect(self.ouvrir_fichier)
        
    def changer_vue(self):
        if self.vue_application.produitVue.isVisible():
            self.vue_application.produitVue.hide()
            self.vue_application.ajout_plan.setText("Ajouter des produits")
            self.trouver_chemin()
            self.vue_application.planVue.show()
        else:
            self.vue_application.produitVue.show()
            self.vue_application.planVue.hide()
            self.vue_application.planVue.supprimer_chemin()
            self.vue_application.ajout_plan.setText("Voir le plan")
            
            
    def trouver_chemin(self):
        points = self.plan.get_plan()
        depart = (1, 1)

        # Trouver le point de départ
        depart_point = None
        for point in points:
            if point.get_coordonnee() == depart:
                depart_point = point
                break
        point_article = []

        for nom_produit in self.panier:
            arrivee_point = None
            for point in points:
                if isinstance(point.get_fonction(), Etagere):
                    etagere = point.get_fonction()
                    if any(produit.get_nom() == nom_produit for produit in etagere.get_produits()):
                        arrivee_point = point
                        break
            
            if arrivee_point and arrivee_point not in point_article:
                point_article.append(arrivee_point)
        
        chemin = self.plan.chemin_rapide(depart_point,point_article)
        self.vue_application.planVue.afficher_chemin(chemin, self.plan.get_l(), self.plan.get_h())
        print(chemin)


    
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
        
        button.clicked.connect(lambda: self.retirer_produit_liste(layout, ligne_separation))
        
        layout.addWidget(label)
        layout.addWidget(button)
        
        if self.vue_application.liste_layout.count() > 1:  # Si il s'agit du premier produit dans la liste, on n'ajoute pas de ligne séparatrice
            self.vue_application.liste_layout.insertWidget(self.vue_application.liste_layout.count() - 1, ligne_separation)
        
        self.vue_application.liste_layout.insertLayout(self.vue_application.liste_layout.count() - 1, layout)
        
        print("produit ajouté : " + nom_produit)



    def retirer_produit_liste(self, layout, ligne_separation):
        
        # Récuperation du nom du produit dans le label pour supprimer le produit du panier
        label = layout.itemAt(0).widget()
        if isinstance(label, QLabel):
            nom_produit = label.text()
            if nom_produit in self.panier:
                self.panier.remove(nom_produit)
                print("Produit retiré : " + nom_produit)
                
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.vue_application.liste_layout.removeItem(layout)
        layout.deleteLater()
        
        ligne_separation.setParent(None)
     
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

    def ouvrir_fichier(self):
        fileName, _ = QFileDialog.getOpenFileName(self.vue_application, "Ouvrir le fichier", "", "JSON Files (*.json);;All Files (*)")
        print(fileName)
        if fileName:
            self.vider_liste()
            self.plan.lire_JSON(fileName)
            self.vue_application.produitVue.charger_produits(self.plan.get_plan())
            self.vue_application.produitVue.filtre1.setCurrentIndex(0)
            self.vue_application.planVue.supprimer_plan()
            self.vue_application.planVue.afficher_plan()

    def reset_application(self):
        self.vue_application.produitVue.reset_vue() # Supprime les produits afficher sur la page
        self.vider_liste()
        self.vue_application.planVue.supprimer_plan()
        self.vue_application.produitVue.reset_vue()
        self.vue_application.planVue.supprimer_chemin()


if __name__ == "__main__":
    controleur = Controleur()
    