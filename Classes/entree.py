import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.fonction import Fonction

class Entree(Fonction):
    def __init__(self, nom : str = None) -> None:
        super().__init__("entree")
        self._nomEntree = nom
    
    def getNomEntree(self) -> str:
        return self._nomEntree
    
    def setNomEntree(self, nouveauNom : str) -> None:
        self._nomEntree = nouveauNom