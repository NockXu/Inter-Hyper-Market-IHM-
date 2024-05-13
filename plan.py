from point import Point
# Cette classe servirat de base à la création du plan des magasins
class Plan :
    def __init__(self, h : int = 9, l : int = 9) -> None:
        # on définit un liste contenant un dictionnaire contenant toutes les coordonnées des point du plan ses voisins et sa fonction dans le magasin (None par défaut)
        self.points : list[Point] = []
        
        # ajout des points dans la liste des points
        for x in range(h):
            for y in range(l):
                self.points.append(Point(x, y))
        
        # Après la création des point on reparcour la liste pour ajouter les voisins de chaque point et inversement ajouter chaque point à ses voisins
        for i in range(len(self.points)):
            self.points[i].voisin(self.points)
            
    
    # méthode qui permet d'ajouter un point dans le plan
    def ajoutPoint(self, x : int, y : int) -> None:
        # on crée le point
        nouveauPoint : Point = Point(x, y)
        
        # on l'ajoute dans le plan
        self.points.append(nouveauPoint)
        
        # on ajoute ses voisins et inversement on l'ajoute à ses voisins
        self.points[-1].voisin(self.points)
        
    def ajoutPlan(self, plan : list) -> None :
        for i in range(len(plan)):
            newPoint = plan[i]
            voisin = newPoint
                
    def __str__(self) -> str:
        texte = "{\n"
        for point in self.points:
            texte += str(point) + "\n"  # Concaténer chaque point converti en chaîne à texte
        
        return texte + "}"



if __name__ == "__main__":
    test = Plan(3, 3)

    print(test)  # Affichage des points initiaux

    test.ajoutPoint(2, 3)

    print("\n",test)  # Affichage après ajout du nouveau point