from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class ImageDeplacement(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._drag_active = False
        self._offset = QPoint()
        self.setMouseTracking(True)
        self.polygon = QPolygon()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._mouse_position = event.position().toPoint()
            self._offset = self._mouse_position - self.pos()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            new_position = event.position().toPoint() - self._offset
            self.move(new_position)
            self.updatePolygon()
            print(f'Position : {self.pos().x()}, {self.pos().y()}')

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = False
            print(f'Image déplacée à la position : {self.pos().x()}, {self.pos().y()}')

    def updatePolygon(self):
        # Mise à jour de la position du polygone
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


    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.polygon.isEmpty():
            painter = QPainter(self)
            pen = QPen(QColor('red'))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawPolygon(self.polygon)