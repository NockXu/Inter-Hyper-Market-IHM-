# Classe qui permet de créer des objet Point qui possède deux attributs x et y
# Cette classe contient aussi des méthodes qui permette de simplifier son interaction avec les autres points du plan
class Point:
    def __init__(self, x: int, y: int, voisins: list = None, fonction : str = None) -> None:
        self.x : int = x
        self.y : int = y
        self.voisins : list = voisins
        self.fonction : str = fonction
    
    # méthode qui renvoie une liste de tout les voisin d'un point à partir d'une liste
    def voisin(self, liste: list, ajoutoppose : bool = True) -> None:
        
        for point in liste:
            if point != self:  # Ignorer le point lui-même
                
                # Vérifier si le point est un voisin (distance de Manhattan = 1)
                if abs(point.x - self.x) + abs(point.y - self.y) == 1:
                    
                    if self.voisins != None:
                        self.voisins.append((point.x, point.y))
                    else:
                        self.voisins = [(point.x, point.y)]
                    
                    # Si on les points sont accessible des deux sens
                    if ajoutoppose:
                        if point.voisins != None:
                            point.voisins.append((self.x, self.y))
                        else:
                            point.voisins = [(self.x, self.y)]
                    
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}) " + f": [voisin : {self.voisins}," + f" fonction : {self.fonction}]"

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
    point1.voisin([point1, point2, point3, point4])
    
    print(point1, point2, point3, point4)