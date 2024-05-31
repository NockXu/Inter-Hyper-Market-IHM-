from PyQt6.QtWidgets import QLabel, QFrame, QApplication, QMainWindow
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen
import sys

class ImageDeplacement(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.deplacement_active = False
        self._offset = QPointF()
        self.setMouseTracking(True)
        self.rects: list[QRectF] = []  # Liste pour stocker les rectangles
        self.rect_colors: dict[int, QColor] = {}  # Dictionnaire pour stocker les couleurs des rectangles
        self.rows = 0
        self.cols = 0
        self.selected_cells = set()
        self.colored_rects = set()  # Ensemble pour stocker les rectangles colorés
        self.brush_color = QColor('black')  # Couleur de base du pinceau

    # Signaux
    getRectsDeclenchee = pyqtSignal(list)
    rectangleTrouvee = pyqtSignal(QRectF)

    def set_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.update_grid()
        self.get_rects()

    def update_grid(self):
        for frame in self.findChildren(QFrame):
            frame.deleteLater()

        self.rects.clear()  # Nettoyer la liste des rectangles
        self.rect_colors.clear()  # Nettoyer le dictionnaire des couleurs
        self.colored_rects.clear()  # Nettoyer la liste des rectangles colorés

        if self.rows > 0 and self.cols > 0:
            cellule_width = self.width() / self.cols
            cellule_height = self.height() / self.rows

            for row in range(self.rows):
                for col in range(self.cols):
                    frame = QFrame(self)
                    frame.setGeometry(int(col * cellule_width), int(row * cellule_height), int(cellule_width), int(cellule_height))
                    frame.setFrameShape(QFrame.Shape.Box)
                    frame.setStyleSheet("background-color: transparent; border: 1px solid blue;")
                    frame.setObjectName(f"frame_{row}_{col}")

                    rect = QRectF(col * cellule_width, row * cellule_height, cellule_width, cellule_height)
                    self.rects.append(rect)

            self.update()

    def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
                for i in range(len(self.rects)):
                    if self.rects[i].contains(event.position()):
                        if i in self.colored_rects:
                            self.colored_rects.remove(i)
                        else:
                            self.colored_rects.add(i)
                        self.update()
                        break

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.pixmap():
            painter.drawPixmap(self.rect(), self.pixmap())

            if self.rows > 0 and self.cols > 0:
                cellule_width = self.width() / self.cols
                cellule_height = self.height() / self.rows

                pen = QPen(QColor('black'))
                pen.setWidth(1)
                painter.setPen(pen)

                for row in range(self.rows + 1):
                    y = int(row * cellule_height)
                    painter.drawLine(0, y, self.width(), y)

                for col in range(self.cols + 1):
                    x = int(col * cellule_width)
                    painter.drawLine(x, 0, x, self.height())

                for i in self.colored_rects:
                    color = self.rect_colors.get(i, self.brush_color)  # Récupérer la couleur du rectangle
                    painter.fillRect(self.rects[i], color)
                    self.rectangleTrouvee.emit(self.rects[i])

    def get_rects(self):
        self.getRectsDeclenchee.emit(self.rects)

    def updateRect(self, index, new_rect):
        self.rects[index] = new_rect
        self.update()

    def clearAll(self):
        self.rows = 0
        self.cols = 0
        self.selected_cells = set()
        self.update_grid()

    def set_brush_color(self, color):
        self.brush_color = color
        self.update()

    def get_rect_color(self, rect: QRectF):
        try:
            index = self.rects.index(rect)
            return self.rect_colors.get(index, None)
        except ValueError:
            return None
        
    def clear_color(self):
        self.selected_cells = set()

# Exemple d'utilisation
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    image_label = ImageDeplacement()
    image_label.set_grid(5, 5)  # Par exemple, une grille 5x5

    main_window.setCentralWidget(image_label)
    main_window.show()

    sys.exit(app.exec())