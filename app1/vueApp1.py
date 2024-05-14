import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        # style d'affichage
        self.app = QApplication(sys.argv)
        fichier_style = open(sys.path[0] + "/qss/style.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.app.setStyleSheet(qss)

        super().__init__()

        #--------------------------------------------------------------------------------

        # Barre d'outils
        self.toolbar = QToolBar('')
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        #--------------------------------------------------------------------------------

        # Ajouter des actions à la barre d'outils
        self.action_nouveau = QAction('Nouveau', self)
        self.toolbar.addAction(self.action_nouveau)

        self.action_ouvrir = QAction('Ouvrir', self)
        self.toolbar.addAction(self.action_ouvrir)

        self.action_enregistrer = QAction('Enregistrer', self)
        self.toolbar.addAction(self.action_enregistrer)

        self.action_supprimer = QAction('Supprimer', self)
        self.toolbar.addAction(self.action_supprimer)

        #--------------------------------------------------------------------------------

        # Ajouter un espace extensible à gauche de la barre d'outils pour aligner les boutons à gauche
        spacer_left = QWidget()
        spacer_left.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer_left)

        # Ajouter un espace extensible à droite de la barre d'outils pour aligner le bouton à droite
        spacer_right = QWidget()
        spacer_right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer_right)

        self.action_reset = QAction('Réinitialiser', self)
        self.toolbar.addAction(self.action_reset)

        #--------------------------------------------------------------------------------

        self.layout_dock = QVBoxLayout()

        self.load_plan_button = QPushButton('Charger un plan')

        self.nom_projet_label = QLabel("Nom de projet :")
        self.nom_projet = QLineEdit()

        self.nom_magasin_label = QLabel('Nom du magasin :')
        self.nom_magasin = QLineEdit()

        self.auteur_label = QLabel('Auteur :')
        self.auteur = QLineEdit()

        self.date_label = QLabel('Date de création :')
        self.date = QDateEdit(calendarPopup=True)
        self.date.setDate(QDate.currentDate())

        self.adresse_label = QLabel('Adresse du magasin :')
        self.adresse = QLineEdit()

        self.layout_dock.addWidget(self.load_plan_button)
        self.layout_dock.addWidget(self.nom_projet_label)
        self.layout_dock.addWidget(self.nom_projet)
        self.layout_dock.addWidget(self.nom_magasin_label)
        self.layout_dock.addWidget(self.nom_magasin)
        self.layout_dock.addWidget(self.auteur_label)
        self.layout_dock.addWidget(self.auteur)
        self.layout_dock.addWidget(self.date_label)
        self.layout_dock.addWidget(self.date)
        self.layout_dock.addWidget(self.adresse_label)
        self.layout_dock.addWidget(self.adresse)

        self.layout_dock.addStretch(1)

        self.layout_right = QHBoxLayout()

        self.plan_label = QLabel()
        self.layout_right.addWidget(self.plan_label)

        self.load_plan_button.clicked.connect(self.load_plan)

        #--------------------------------------------------------------------------------

        self.outil = QWidget()
        self.outil.setLayout(self.layout_dock)

        #--------------------------------------------------------------------------------

        self.layout_groupe = QHBoxLayout()

        self.layout_groupe.addLayout(self.layout_right)

        self.widget_centre = QWidget()
        self.widget_centre.setLayout(self.layout_groupe)
        self.setCentralWidget(self.widget_centre)

        #--------------------------------------------------------------------------------

        self.dock1 = QDockWidget("Menu Outil")
        self.dock1.setWidget(self.outil)
        self.dock1.setFixedWidth(300)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock1)

        #--------------------------------------------------------------------------------

        # Paramètres d'affichage
        self.setWindowTitle('INTER-HYPER-MARKET')
        self.showMaximized()
        self.show()

    def load_plan(self):
        # Ouvre une boîte de dialogue pour sélectionner une image
        file_name, _ = QFileDialog.getOpenFileName(self, "Charger un plan", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_name:
            # Affiche l'image sélectionnée dans le QLabel du layout droit
            pixmap = QPixmap(file_name)
            self.plan_label.setPixmap(pixmap)
            self.plan_label.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
