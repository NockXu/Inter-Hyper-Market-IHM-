import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen

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

    def extraire_chemin(self, chemin_complet, sous_chemin):
        index = chemin_complet.find(sous_chemin)
        if index != -1:
            return chemin_complet[index:]
        else:
            return None

    def afficher_plan(self, image):
        sous_chemin = "Magasin"
        chemin_relatif = self.extraire_chemin(image, sous_chemin)
        if chemin_relatif:
            self.image = QPixmap(chemin_relatif)
            self.update()
        else:
            print("Sous-chemin non trouvé dans le chemin complet.")

    def supprimer_plan(self):
        self.image = None
        self.update
        
    def supprimer_chemin(self):
        self.rects.clear()
        self.chemins.clear()
        self.rows = 0
        self.cols = 0
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.largeur = self.width()
        self.longueur = self.height()
        self.update_grid()

    def update_grid(self):
        self.rects.clear()
        if self.rows > 0 and self.cols > 0:
            cell_width = self.largeur / self.cols
            cell_height = self.longueur / self.rows
            

            for row in range(self.rows):
                for col in range(self.cols):
                    rect = QRectF(col * cell_width, row * cell_height, cell_width, cell_height)
                    self.rects[(row, col)] = rect
        self.update()

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
            pen.setWidth(20)
            painter.setPen(pen)
            for i in range(len(chemin) - 1):
                start_point = self.rects[chemin[i]].center()
                end_point = self.rects[chemin[i + 1]].center()
                painter.drawLine(start_point, end_point)

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
