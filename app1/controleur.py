# controller.py
import sys
from PyQt6.QtWidgets import QApplication
from vueApp1 import MainWindow
from Classes import Plan

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