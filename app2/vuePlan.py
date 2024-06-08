import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen, QFont

class VuePlan(QWidget):
    def __init__(self):
        super().__init__()

        self.rects = {}
        self.rows = 0
        self.cols = 0
        self.chemins = []
        self.image = None
        self.largeur = self.width()
        self.longueur = self.height()

    # Extraction du chemin de fichier pour récuperer un chemin utilisable
    def extraire_chemin(self, chemin_complet, sous_chemin):
        index = chemin_complet.find(sous_chemin)
        if index != -1:
            return chemin_complet[index:]
        else:
            return None

    # Affichage de l'image du plan
    def afficher_plan(self, image):
        sous_chemin = "Magasin"
        chemin_relatif = self.extraire_chemin(image, sous_chemin)
        if chemin_relatif:
            self.image = QPixmap(chemin_relatif)
            self.update()
        else:
            print("Sous-chemin non trouvé dans le chemin complet.")

    # Supprime l'image du plan en lui implantant la valeur None 
    def supprimer_plan(self):
        self.image = None
        self.update()
        
    # Suppression du chemin et de la valeur des lignes et colonnes
    def supprimer_chemin(self):
        self.rects.clear()
        self.chemins.clear()
        self.rows = 0
        self.cols = 0
        self.update()

    # Fonction qui redimentionne la grille du plan à la taille de la fenetre
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.largeur = self.width()
        self.longueur = self.height()
        self.update_grid()

    # Fonction de mise à jour de la taille des lignes et colonnes 
    def update_grid(self):
        self.rects.clear()
        if self.rows > 0 and self.cols > 0:
            cell_width = self.largeur / self.cols # Largeur d'une case est égale à la taille de la page par le nombre de colonnes
            cell_height = self.longueur / self.rows # Longueur d'une case est égale à la taille de la page par le nombre de lignes
            
            for row in range(self.rows):
                for col in range(self.cols):
                    rect = QRectF(col * cell_width, row * cell_height, cell_width, cell_height)
                    self.rects[(row, col)] = rect
        self.update()

    # Fonction qui affiche le chemin et la grille en suppreposition sur l'image du plan
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.image:
            scaled_image = self.image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(self.rect(), scaled_image)

        pen = QPen(QColor("black"))
        pen.setWidth(1)
        painter.setPen(pen)

        # Dessiner le quadrillage
        for rect in self.rects.values():
            painter.drawRect(rect)

        # Dessiner les chemins
        for chemin in self.chemins:
            pen.setColor(QColor("red"))
            pen.setWidth(30)
            painter.setPen(pen)
            for i in range(len(chemin) - 1):
                start_point = self.rects[chemin[i]].center()
                end_point = self.rects[chemin[i + 1]].center()
                painter.drawLine(start_point, end_point)
            
            # Ajouter le texte "entrée" au premier point du chemin
            if chemin:
                entree_point = self.rects[chemin[0]].center()
                painter.setPen(QPen(QColor("black")))
                font = QFont()
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(entree_point, "Entrée")

    # Initalisation du nombre de lignes et colonnes
    def afficher_chemin(self, chemins, rows, cols):
        self.rows = rows
        self.cols = cols
        self.chemins = chemins
        self.update_grid()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = VuePlan()
    fenetre.show()
    
    sys.exit(app.exec())
