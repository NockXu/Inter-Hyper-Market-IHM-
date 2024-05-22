import sys, os
from PyQt6.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QFrame, QLabel, QPushButton
from vueApplication import VueApplication

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Controleur:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.vue_application = VueApplication(self)
        self.connect_signals()
        self.vue_application.show()
        sys.exit(self.app.exec())

    def connect_signals(self):
        self.vue_application.ajout_plan.clicked.connect(self.changer_vue)
        self.vue_application.produit_ajoute.connect(self.ajouter_produit_liste)
        self.vue_application.magasin.clicked.connect(self.ouvrir_fichier)
        self.vue_application.supp.clicked.connect(self.vider_liste)
        self.vue_application.action_reset.triggered.connect(self.reset_application)
        
    def changer_vue(self):
        if self.vue_application.produitVue.isVisible():
            self.vue_application.produitVue.hide()
            self.vue_application.ajout_plan.setText("Ajouter des produits")
            self.vue_application.planVue.show()
        else:
            self.vue_application.produitVue.show()
            self.vue_application.planVue.hide()
            self.vue_application.ajout_plan.setText("Voir le plan")
    
    def ajouter_produit_liste(self, nom_produit):
        layout = QHBoxLayout()
        
        label = QLabel(nom_produit)
        button = QPushButton("X")
        button.setFixedWidth(30)
        button.setFixedHeight(30)
        
        ligne_separation = QFrame()
        ligne_separation.setFrameShape(QFrame.Shape.HLine)
        ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
        
        button.clicked.connect(lambda: self.retirer_produit_liste(layout, ligne_separation))
        
        layout.addWidget(label)
        layout.addWidget(button)
        
        if self.vue_application.liste_layout.count() > 1:  # Si il sagit du premier produit dans la liste, on n'ajoute pas de ligne separatrice
            self.vue_application.liste_layout.insertWidget(self.vue_application.liste_layout.count() - 1, ligne_separation)
        
        self.vue_application.liste_layout.insertLayout(self.vue_application.liste_layout.count() - 1, layout)
        
        print("produit ajouté : " + nom_produit)

    def retirer_produit_liste(self, layout, ligne_separation):
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
            if isinstance(item, QHBoxLayout):
                self.retirer_produit_liste(item, item.itemAt(1).widget())
            elif isinstance(item.widget(), QFrame):
                item.widget().setParent(None)
            else:
                self.vue_application.liste_layout.removeItem(item)
                item.widget().deleteLater()

    def ouvrir_fichier(self):
        fileName, _ = QFileDialog.getOpenFileName(self.vue_application, "Ouvrir le fichier", "", "All Files (*);;Text Files (*.txt)")
        if fileName:
            self.vider_liste()
            self.vue_application.produitVue.charger_produits(fileName)
            self.vue_application.produitVue.filtre1.setCurrentIndex(0)

    def reset_application(self):
        self.vider_liste()
        self.vue_application.produitVue.reset_vue()

if __name__ == "__main__":
    controleur = Controleur()
