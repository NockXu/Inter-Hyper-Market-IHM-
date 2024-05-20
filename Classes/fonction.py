from .accessibilite import Accessibilite

class Fonction:
    def __init__(self, nom : str = "None"):
        self._acces : Accessibilite = Accessibilite()
        self._nom : str = nom # il n'y a pas de setter car le nom n'est pas choisis par l'utilisateur
    
    # Méthodes getters
    
    def getHaut(self) -> bool:
        return self._acces.get_H()
    
    def getBas(self) -> bool:
        return self._acces.get_B()
    
    def getGauche(self) -> bool:
        return self._acces.get_G()
    
    def getDroite(self) -> bool:
        return self._acces.get_D()
    
    # récupère le nom de la fonction
    def getNom(self) -> str:
        return self._nom
    
    # Méthodes setters
    
    def setHaut(self, H : bool = True) -> None:
        return self._acces.set_H(H)
    
    def setBas(self, B : bool = True) -> None:
        return self._acces.set_B(B)
    
    def setGauche(self, G : bool = True) -> None:
        return self._acces.set_G(G)
    
    def setDroite(self, D : bool = True) -> None:
        return self._acces.set_D(D)
    
    # Méthode spéciale __str__()
    def __str__(self) -> str:
        return "{"+f" nom : {self._nom}, {self._acces}"+"}"
    
    # Méthode spéciale __eq__()
    def __eq__(self, other) -> bool:
        if not isinstance(other, Fonction):
            return False
        return self._nom == other._nom and self._acces == other._acces