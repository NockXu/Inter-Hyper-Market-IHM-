from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen

class ImageDeplacement(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.deplacement_active = False
        self._offset = QPointF()
        self.setMouseTracking(True)
        self.rects = []  # Liste pour stocker les rectangles
        self.rows = 0
        self.cols = 0
        self.selected_cells = set()
    
    # Signaux
    getRectsDeclenchee = pyqtSignal(list)

    def set_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.update_grid() 
        self.get_rects()

    def update_grid(self):
        for frame in self.findChildren(QFrame):
            frame.deleteLater()

        self.rects.clear()  # Nettoyer la liste des rectangles

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

                    # Créer un rectangle pour chaque cellule
                    rect = QRectF(col * cell_width, row * cell_height, cell_width, cell_height)

                    # Ajouter le rectangle à la liste
                    self.rects.append(rect)

            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.rects:
                painter = QPainter(self)
                painter.setBrush(QColor(255, 192, 203))  # Rose
                for rect in self.rects:
                    painter.drawRect(rect)

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
