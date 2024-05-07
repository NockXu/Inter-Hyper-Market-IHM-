# Classe qui permet de créer des objet Point qui possède deux attributs x et y
# Cette classe contient aussi des méthodes qui permette de simplifier son interaction avec les autres points du plan
class Point:
    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y
    
    # méthode qui renvoie une liste de tout les voisin d'un point à partir d'une liste
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    
    def voisin(self, liste: list[dict]) -> list:
        voisins = []
        
        for point_info in liste:
            if point_info["coordonnees"] != self:  # Ignorer le point lui-même
                coord = point_info["coordonnees"]
                
                # Vérifier si le point est un voisin (distance de Manhattan = 1)
                if abs(coord.x - self.x) + abs(coord.y - self.y) == 1:
                    voisins.append(coord)
        
        return voisins
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

# Exemple d'utilisation de la classe Point
if __name__ == "__main__":
    # Création de quelques points
    point1 = Point(0, 0)
    point2 = Point(1, 0)
    point3 = Point(0, 1)
    point4 = Point(2, 0)
    
    # Liste de points (dictionnaires contenant les informations des points)
    liste_points = [
        {"coordonnees": point1},
        {"coordonnees": point2},
        {"coordonnees": point3},
        {"coordonnees": point4}
    ]
    
    # Utilisation de la méthode voisin pour le point1 parmi la liste de points
    voisins_point1 = point1.voisin(liste_points)
    
    print(f"Voisins de {point1}: {[str(point) for point in voisins_point1]}")