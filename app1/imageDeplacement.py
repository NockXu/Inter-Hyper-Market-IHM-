from PyQt6.QtWidgets import QLabel, QFrame, QApplication, QMainWindow
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen
import sys

class ImageDeplacement(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMouseTracking(True)
        self.rects = {}
        self.rows = 0
        self.cols = 0
        self.brush_color = QColor("white")
        self.brush_color.setAlpha(0)
        
        # Pour les fonctions
        self.est_fonction = True
        self.fonction_actuelle : str = None
        
        self.chemin = QColor('red')
        self.chemin.setAlpha(128)
        
        self.entree = QColor('green')
        self.entree.setAlpha(128)
        
        self.etagere = QColor('blue')
        self.etagere.setAlpha(128)

    # Signaux
    getRectsDeclenchee = pyqtSignal(list)
    rectColoriee = pyqtSignal(tuple)
    rectFoncAttribuee = pyqtSignal(tuple)
    rectFoncSupprimee = pyqtSignal(tuple)
    etagereAjoutee = pyqtSignal(tuple)
    etagereSupprimee = pyqtSignal(tuple)
    

    def set_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.update_grid()
        self.get_rects()

    def update_grid(self):
        self.rects.clear()

        if self.rows > 0 and self.cols > 0:
            cellule_width = self.width() / self.cols
            cellule_height = self.height() / self.rows

            for row in range(self.rows):
                for col in range(self.cols):
                    rect = QRectF(col * cellule_width, row * cellule_height, cellule_width, cellule_height)
                    color = QColor("white")
                    color.setAlpha(0)
                    self.rects[(row, col)] = {"rect": rect, "color": color, "fonction" : None}

            self.update()

    def getColorFonc(self, name : str) -> QColor:
        if name == "chemin":
            color = self.chemin
        elif name == "entree":
            color = self.entree
        elif name == "etagere":
            color = self.etagere
        else:
            color = QColor("white")
            color.setAlpha(0)
        return color
    
    def setChemin(self, color : QColor) -> None:
        color.setAlpha(128)
        self.chemin = color
        
    def setEntree(self, color : QColor) -> None:
        color.setAlpha(128)
        self.entree = color
        
    def setEtagere(self, color : QColor) -> None:
        color.setAlpha(128)
        self.etagere = color

    def ajouter_etagere(self, position):
        """
        Ajoute une étagère à la position spécifiée.
        """
        self.etagereAjoutee.emit(position)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for rect in self.rects.keys():
                if self.rects[rect]["rect"].contains(event.position()):
                    color = QColor("white")
                    color.setAlpha(0)
                    # Cas d'attribution de couleur de fonction
                    if self.est_fonction:
                        if self.rects[rect]["fonction"] == self.fonction_actuelle:
                            self.rects[rect]["fonction"] = color
                            self.rectFoncSupprimee.emit(rect)
                            self.etagereSupprimee.emit(rect)
                        else:
                            self.rects[rect]["fonction"] = self.fonction_actuelle
                            self.rectFoncAttribuee.emit(rect)
                            self.ajouter_etagere(rect)
                    # Cas d'attribution de couleur de rayon
                    else:
                        if self.rects[rect]["color"] == self.brush_color:
                            self.rects[rect]["color"] = color
                        else:
                            self.rects[rect]["color"] = self.brush_color
                            self.rectColoriee.emit(rect)
                    self.update()
                    return

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.pixmap():
            painter.drawPixmap(self.rect(), self.pixmap())

        pen = QPen(QColor("black"))
        pen.setWidth(1)
        painter.setPen(pen)

        for rect in self.rects.keys():
            if self.est_fonction:  
                painter.fillRect(self.rects[rect]["rect"], self.getColorFonc(self.rects[rect]["fonction"]))
            else:
                painter.fillRect(self.rects[rect]["rect"], self.rects[rect]["color"])
            painter.drawRect(self.rects[rect]["rect"])

    def get_rects(self):
        self.getRectsDeclenchee.emit(self.rects)

    def updateRect(self, index, new_rect):
        self.rects[index] = new_rect
        self.update()

    def clearAll(self):
        self.rows = 0
        self.cols = 0
        self.update_grid()

    def updateColor(self, rects: dict[tuple[int, int], QColor]):
        for point in rects.keys():
            if point in self.rects:
                self.rects[point]["color"] = rects[point]
        self.update()

    def set_brush_color(self, color : QColor):
        color.setAlpha(128)
        self.brush_color = color
        self.update()
    
    def switch_est_fonction(self) -> None:
        self.est_fonction = not self.est_fonction
        self.update()
    
    def set_fonction_actuelle(self, chemin : bool, entree : bool, etagere : bool) -> None:
        if chemin:
            self.fonction_actuelle = 'chemin'
        elif entree:
            self.fonction_actuelle = 'entree'
        elif etagere:
            self.fonction_actuelle = 'etagere'
        else:
            self.fonction_actuelle = None

# Exemple d'utilisation
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    image_label = ImageDeplacement()
    image_label.set_grid(5, 5)  # Par exemple, une grille 5x5

    main_window.setCentralWidget(image_label)
    main_window.show()

    sys.exit(app.exec())
