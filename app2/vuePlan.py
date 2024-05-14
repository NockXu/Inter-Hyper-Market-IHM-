import sys
from PyQt6.QtWidgets import QWidget, QFileDialog, QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap

class VuePlan(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # QLabel pour afficher l'image
        self.plan_label = QLabel()
        self.layout.addWidget(self.plan_label)

        # Bouton pour charger l'image
        self.btn_load_plan = QPushButton("Charger un plan")
        self.btn_load_plan.clicked.connect(self.load_plan)
        self.layout.addWidget(self.btn_load_plan)

    def load_plan(self):
        # Ouvre une boîte de dialogue pour sélectionner une image
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger un plan", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_name:
            # Affiche l'image sélectionnée dans le QLabel
            pixmap = QPixmap(file_name)
            self.plan_label.setPixmap(pixmap)
            self.plan_label.setScaledContents(True)
            
        self.setWindowTitle('Application client')
        self.showMaximized() 

if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VuePlan()
    fenetre.show()
    sys.exit(app.exec())
