from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFormLayout, QApplication, QColorDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from bouton import Bouton

class FonctionRect(QWidget):
    
    # Signaux
    boutonCliquee = pyqtSignal(bool, bool, bool)
    modeChangee = pyqtSignal()
    fonctionSelectionnee = pyqtSignal(str, QColor)
    
    def __init__(self):
        super().__init__()

        # Initialisation des composants de layout_fonction
        self.bouton_fonction = QPushButton('Désactiver mode fonction')
        self.bouton_fonction.clicked.connect(self.toggle_mode)

        self.chemin_active = False
        self.entree_active = False
        self.etagere_active = False
        self.mode_fonction = True

        self.bouton_chemin = Bouton('red')
        self.bouton_entree = Bouton('green')
        self.bouton_etagere = Bouton('blue')

        self.bouton_chemin_label = self.create_label_button('Chemin', 'chemin')
        self.bouton_entree_label = self.create_label_button('Entrée', 'entree')
        self.bouton_etagere_label = self.create_label_button('Étagère', 'etagere')

        # Layout pour les fonctionnalités
        self.layout_fonction = QVBoxLayout()
        self.layout_form = QFormLayout()

        self.layout_fonction.addWidget(self.bouton_fonction)

        self.layout_form.addRow(self.bouton_chemin, self.bouton_chemin_label)
        self.layout_form.addRow(self.bouton_entree, self.bouton_entree_label)
        self.layout_form.addRow(self.bouton_etagere, self.bouton_etagere_label)
        self.layout_form.setVerticalSpacing(20)
        self.layout_form.setHorizontalSpacing(20)

        self.layout_fonction.addLayout(self.layout_form)
        
        self.setLayout(self.layout_fonction)

    def create_label_button(self, text, label_name):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.set_active(label_name))
        return button

    def set_active(self, label_name):
        if label_name == 'chemin':
            self.chemin_active = True
            self.entree_active = False
            self.etagere_active = False
            self.fonctionSelectionnee.emit("chemin", self.bouton_chemin.get_color())
        elif label_name == 'entree':
            self.chemin_active = False
            self.entree_active = True
            self.etagere_active = False
            self.fonctionSelectionnee.emit("entree", self.bouton_entree.get_color())
        elif label_name == 'etagere':
            self.chemin_active = False
            self.entree_active = False
            self.etagere_active = True
            self.fonctionSelectionnee.emit("etagere", self.bouton_etagere.get_color())
        self.boutonCliquee.emit(self.chemin_active, self.entree_active, self.etagere_active)

    def toggle_mode(self):
        self.mode_fonction = not self.mode_fonction
        if self.mode_fonction:
            self.bouton_fonction.setText('Désactiver mode fonction')
            self.bouton_chemin.show()
            self.bouton_entree.show()
            self.bouton_etagere.show()
            self.bouton_chemin_label.show()
            self.bouton_entree_label.show()
            self.bouton_etagere_label.show()
        else:
            self.bouton_fonction.setText('Activer mode fonction')
            self.bouton_chemin.hide()
            self.bouton_entree.hide()
            self.bouton_etagere.hide()
            self.bouton_chemin_label.hide()
            self.bouton_entree_label.hide()
            self.bouton_etagere_label.hide()
        self.modeChangee.emit()

# Exemple d'utilisation
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = FonctionRect()
    widget.show()
    sys.exit(app.exec())
