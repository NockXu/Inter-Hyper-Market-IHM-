from fonction import Fonction
from chemin import Chemin
from etagere import Etagere
from entree import Entree
# Classe qui permet de créer des objet Point qui possède deux attributs x et y
# Cette classe contient aussi des méthodes qui permette de simplifier son interaction avec les autres points du plan
class Point:
    def __init__(self, x: int, y: int, voisins: list = None, fonction: Fonction = Chemin()) -> None:
        self._x : int = x
        self._y : int = y
        self._voisins : list = voisins
        self._fonction : Fonction = fonction
    
    # Méthodes getters
    def get_x(self) -> int:
        return self._x
    
    def get_y(self) -> int:
        return self._y
    
    def get_voisins(self) -> list:
        return self._voisins
    
    def get_fonction(self) -> Fonction:
        return self._fonction
    
    def getHaut(self) -> bool:
        return self._fonction.getHaut()
    
    def getBas(self) -> bool:
        return self._fonction.getBas()
    
    def getGauche(self) -> bool:
        return self._fonction.getGauche()
    
    def getDroite(self) -> bool:
        return self._fonction.getDroite()

    # Méthodes setters
    def set_x(self, x: int) -> None:
        self._x = x
    
    def set_y(self, y: int) -> None:
        self._y = y
    
    def set_fonction(self, fonction: str) -> None:
        self._fonction = fonction

    # Méthode qui renvoie une liste de tous les voisins d'un point à partir d'une liste donnée
    def set_voisins(self, liste: list, ajoutoppose: bool = True) -> None:
        for point in liste:
            if point != self:  # Ignorer le point lui-même
                # Vérifier si le point est un voisin (distance de Manhattan = 1)
                if abs(point._x - self._x) + abs(point._y - self._y) == 1:
                    if self._voisins is None:
                        self._voisins = [(point._x, point._y)]
                    else:
                        self._voisins.append((point._x, point._y))
                    
                    # Si les points sont accessibles dans les deux sens
                    if ajoutoppose:
                        if point._voisins is None:
                            point._voisins = [(self._x, self._y)]
                        else:
                            point._voisins.append((self._x, self._y))
    
    def setHaut(self, H : bool = True) -> None:
        return self._fonction.setHaut(H)
    
    def setBas(self, B : bool = True) -> None:
        return self._fonction.setBas(B)
    
    def setGauche(self, G : bool = True) -> None:
        return self._fonction.setGauche(G)
    
    def setDroite(self, D : bool = True) -> None:
        return self._fonction.setDroite(D)

    # Méthode spéciale __str__()
    def __str__(self) -> str:
        return f"({self._x}, {self._y}) : [voisins : {self._voisins}, fonction : {self._fonction}]"

    # Méthode spéciale __eq__()
    def __eq__(self, other) -> bool:
        if isinstance(other, Point):  # Vérifie si 'other' est une instance de la classe Point
            return (self._x == other._x) and (self._y == other._y)
        return False

# Exemple d'utilisation de la classe Point
if __name__ == "__main__":
    # Création de quelques points
    point1 = Point(0, 0)
    point2 = Point(1, 0)
    point3 = Point(0, 1)
    point4 = Point(2, 0)
    
    # Affichage des points
    print(point1, point2, point3, point4)
    
    # ajout des voisins du point 1
    point1.set_voisins([point1, point2, point3, point4])
    
    print(point1, point2, point3, point4)
    
    