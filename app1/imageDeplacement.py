from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QPoint, QRect, QPointF
from PyQt6.QtGui import QPixmap, QPolygon, QPolygonF, QPainter, QPen, QColor

class ImageDeplacement(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.deplacement_active = False
        self._offset = QPoint()
        self.setMouseTracking(True)
        self.polygon = QPolygon()
        self.polygons = []

    def set_polygons(self, polygons):
        self.polygons = polygons

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pixmap_rect = self.getPixmapRect()
            if pixmap_rect.contains(event.position().toPoint()):
                self.deplacement_active = True
                # L'offset est la position de la souris dans le widget au moment du clic
                self._offset = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.deplacement_active:
            # Calculer la nouvelle position en fonction de l'offset
            new_position = self.mapToParent(event.pos() - self._offset)
            self.move(new_position)
            self.updatePolygon()
            print(f'Position : {self.pos().x()}, {self.pos().y()}')

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.deplacement_active = False
            print(f'Image déplacée à la position : {self.pos().x()}, {self.pos().y()}')

    def updatePolygon(self):
        if not self.pixmap():
            return
        rect = self.pixmap().rect()
        top_left = self.rect().topLeft() + QPoint((self.rect().width() - rect.width()) // 2, (self.rect().height() - rect.height()) // 2)
        bottom_right = top_left + QPoint(rect.width(), rect.height())
        points = [
            top_left,
            QPoint(bottom_right.x(), top_left.y()),
            bottom_right,
            QPoint(top_left.x(), bottom_right.y())
        ]
        self.polygon = QPolygon(points)

    def getPixmapRect(self):
        if not self.pixmap():
            return QRect()
        rect = self.pixmap().rect()
        rect.moveCenter(self.rect().center())
        return rect

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.pixmap():
            painter = QPainter(self)
            if self.polygons:
                pen = QPen(QColor('blue'))
                pen.setWidth(1)
                painter.setPen(pen)
                for polygon in self.polygons:
                    painter.drawPolygon(polygon)
            if not self.polygon.isEmpty():
                pen = QPen(QColor('red'))
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawPolygon(self.polygon)

    def clearAll(self):
        self.polygons = []
        self.polygon = QPolygon()
        self.update()
