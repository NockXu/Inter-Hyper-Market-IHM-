from .chemin import Chemin

class Entree(Chemin):
    def __init__(self, nom : str = None) -> None:
        super().__init__("entrée")
        self._nomEntree = nom
    
    def getNomEntree(self) -> str:
        return self._nomEntree
    
    def setNomEntree(self, nouveauNom : str) -> None:
        self._nomEntree = nouveauNom