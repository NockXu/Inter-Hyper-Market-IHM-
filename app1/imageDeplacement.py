from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt, QPointF, pyqtSignal
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
    
    #signaux
    getPolygonDeclanchee = pyqtSignal(list)

    def set_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.update_grid() 
        self.add_polygon()

    def update_grid(self):
        for frame in self.findChildren(QFrame):
            frame.deleteLater()

        self.polygons.clear() 

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

                    # Point des polygones
                    top_left = QPointF(col * cell_width, row * cell_height)
                    top_right = QPointF((col + 1) * cell_width, row * cell_height)
                    bottom_right = QPointF((col + 1) * cell_width, (row + 1) * cell_height)
                    bottom_left = QPointF(col * cell_width, (row + 1) * cell_height)
                    
                    polygon = QPolygonF([top_left, top_right, bottom_right, bottom_left])
                    
                    # Ajout du polygon a la liste
                    self.polygons.append(polygon)

            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            point = event.position()
            for index, polygon in enumerate(self.polygons):
                if polygon.containsPoint(point, Qt.FillRule.WindingFill):
                    print(f"Clicked on polygon at index {index}, position: {point}")
                    polygon_points = self.get_polygon_points(index)
                    for i, pt in enumerate(polygon_points):
                        print(f"Point {i}: ({pt.x()}, {pt.y()})")
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
    
    def add_polygon(self):
        self.getPolygonDeclanchee.emit(self.polygons)

    def updatePolygon(self, index, new_polygon):
        self.polygons[index] = new_polygon
        self.update()

    def clearAll(self):
        self.rows = 0
        self.cols = 0
        self.selected_cells = set()
        self.update_grid()
