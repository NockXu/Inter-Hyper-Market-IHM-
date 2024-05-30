from PyQt6.QtWidgets import QFrame

class LineFrame(QFrame):
    def __init__(self, orientation='horizontal', parent=None):
        super().__init__(parent)
        self.initUI(orientation)

    def initUI(self, orientation):
        if orientation == 'horizontal':
            self.setFrameShape(QFrame.Shape.HLine)
        elif orientation == 'vertical':
            self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
