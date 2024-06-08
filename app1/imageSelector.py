from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ImageSelector(QWidget):
    imageSelectionnee = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        # Créer un bouton pour choisir l'image (avec une icône de dossier)
        self.btn = QPushButton('', self)
        self.btn.setIcon(QIcon('app1/images/file.png'))  # Assurez-vous que vous avez une icône de dossier à utiliser
        self.btn.clicked.connect(self.showDialog)
        
        # Créer un QLineEdit pour afficher et modifier le chemin du fichier
        self.lineEdit = QLineEdit(self)
        
        # Disposer les widgets horizontalement
        hbox = QHBoxLayout()
        hbox.setSpacing(0)  # Retirer l'espacement entre les widgets
        hbox.addWidget(self.lineEdit)
        hbox.addWidget(self.btn)
        
        # Disposer l'ensemble de manière centrale dans la fenêtre
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        # Configurer la fenêtre principale
        self.setWindowTitle('Choisir une image PNG')
        self.setGeometry(300, 300, 400, 100)
        
        # Connecter les signaux
        self.lineEdit.returnPressed.connect(self.getImage)
        
    def showDialog(self):
        # Obtenir le répertoire deux niveaux en arrière du répertoire du fichier actuel
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Magasin/', 'images/'))
        
        # Ouvrir la boîte de dialogue de fichier pour choisir une image PNG
        fileName, _ = QFileDialog.getOpenFileName(self, 'Choisir une image PNG', project_root, 'Images PNG (*.png)')
        if fileName:
            # Mettre à jour le QLineEdit avec le chemin du fichier choisi
            self.lineEdit.setText(fileName)
            self.getImage()
            
    def getImage(self):
        # Récupérer le chemin du fichier depuis le QLineEdit
        filePath = self.lineEdit.text()
        if os.path.isfile(filePath) and filePath.lower().endswith('.png'):
            self.imageSelectionnee.emit(filePath)
        else:
            self.showError("Le fichier spécifié n'est pas une image PNG valide.")
            
    def setImage(self, image : str):
        if image:
            self.lineEdit.setText(image)
            self.imageSelectionnee.emit(image)
    
    def showError(self, message):
        # Afficher une boîte de dialogue d'erreur
        errorMsg = QMessageBox()
        errorMsg.setIcon(QMessageBox.Icon.Critical)
        errorMsg.setWindowTitle('Erreur')
        errorMsg.setText(message)
        errorMsg.exec()
        
    def clear(self):
        self.lineEdit.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSelector()
    ex.show()
    sys.exit(app.exec())
