from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPixmap, QPolygonF, QColor, QPen

class ImageDeplacement(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.deplacement_active = False
        self._offset = QPointF()
        self.setMouseTracking(True)
        self.polygons = []
        self.rows = 0
        self.cols = 0
        self.selected_cells = set()

    def set_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.update_grid()

    def update_grid(self):
        for frame in self.findChildren(QFrame):
            frame.deleteLater()

        if self.rows > 0 and self.cols > 0:
            cell_width = self.width() / self.cols
            cell_height = self.height() / self.rows

            for row in range(self.rows):
                for col in range(self.cols):
                    frame = QFrame(self)
                    frame.setGeometry(int(col * cell_width), int(row * cell_height), int(cell_width), int(cell_height))
                    frame.setFrameShape(QFrame.Shape.Box)
                    frame.setStyleSheet("background-color: transparent; border: 1px solid blue;")
                    frame.setObjectName(f"frame_{row}_{col}")

            self.update()  # Ajout de l'appel à update() pour que les changements soient appliqués

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for frame in self.findChildren(QFrame):
                if frame.geometry().contains(event.position().toPoint()):
                    frame_name = frame.objectName()
                    row, col = map(int, frame_name.split('_')[1:])
                    index = row * self.cols + col
                    if index in self.selected_cells:
                        self.selected_cells.remove(index)
                    else:
                        self.selected_cells.add(index)
                    self.update()
                    break

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.pixmap():
            # Dessiner l'image
            painter.drawPixmap(self.rect(), self.pixmap())

            # Dessiner le quadrillage
            if self.rows > 0 and self.cols > 0:
                cell_width = self.width() / self.cols
                cell_height = self.height() / self.rows

                pen = QPen(QColor('blue'))
                pen.setWidth(1)
                painter.setPen(pen)

                for row in range(self.rows + 1):
                    y = int(row * cell_height)
                    painter.drawLine(0, y, self.width(), y)

                for col in range(self.cols + 1):
                    x = int(col * cell_width)
                    painter.drawLine(x, 0, x, self.height())

    def updatePolygon(self, index, new_polygon):
        self.polygons[index] = new_polygon
        self.update()

    def clearAll(self):
        self.rows = 0
        self.cols = 0
        self.selected_cells = set()
        self.update_grid()
