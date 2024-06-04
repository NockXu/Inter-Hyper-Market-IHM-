import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *


class VuePlan(QWidget):
    def __init__(self):
        super().__init__()
        
##########################################################
#                                                        #
#                   Widgets / Layout                     #
#                                                        #
##########################################################

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.plan = QLabel()
        self.plan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.plan)
        
##########################################################
#                                                        #
#                      Fonctions                         #
#                                                        #
########################################################## 
    
    # Fonction qui affiche l'image du plan du magasin    
    def afficher_plan(self):
        image = QPixmap('app2/image/plan9.jpg')
        scaled_image = image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.plan.setPixmap(scaled_image)
        self.plan.setScaledContents(True)
     
    # Fonction qui efface ce qui se trouve dans plan   
    def supprimer_plan(self):
        if not self.plan.pixmap().isNull():
            self.plan.clear()
        
    def afficher_chemin(self, chemin :list[list[Point]]):
        pass


if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VuePlan()
    fenetre.show()
    sys.exit(app.exec())
