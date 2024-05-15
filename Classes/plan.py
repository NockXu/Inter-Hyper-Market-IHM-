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
            self.points[i].set_voisins(self.points)
            
    # méthode mettant à jour la totalitée des voisins pour tout les points      
    def set_voisinage(self) -> None:
        for point in self.points:
            point.set_voisins(self.points)
            
    # méthode qui permet d'ajouter un point dans le plan
    def ajoutPoint(self, x : int, y : int) -> None:
        # on crée le point
        nouveauPoint : Point = Point(x, y)
        
        # on l'ajoute dans le plan
        self.points.append(nouveauPoint)
        
        # on ajoute ses voisins et inversement on l'ajoute à ses voisins
        self.points[-1].set_voisins(self.points)
    
    # méthode qui permet d'ajouter un plan dans un autre  
    def ajoutPlan(self, plan : list) -> None :
        
        # pour chaque point dans plan
        for point in plan:
            
            # on ajoute le point dans le plan
            self.points.append(point)
            
            # on met à jour les voisins
            self.points[-1].set_voisins(self.points)
    
    # méthode qui permet de supprimer un point du plan si il existe
    def suppPoint(self, suppression : Point) -> None :
        # Parcourir la liste de point pour supprimer le point correspondant à suppression
        for point in self.points:
            if point == suppression:
                self.points.remove(point)
    
    # méthode qui permet de supprimer les point d'un plan à partir d'une liste de point        
    def suppPlan(self, suppression : list) -> None :
        for point in suppression:
            self.suppPoint(point)
                
    def __str__(self) -> str:
        texte = "{\n"
        for point in self.points:
            texte += str(point) + "\n"  # Concaténer chaque point converti en chaîne à texte
        
        return texte + "}"

    def __eq__(self, other):
        if isinstance(other, Plan):  # Vérifie si 'other' est une instance de la classe Plan
            # Comparaison des listes de points
            return self.points == other.points
        return False



if __name__ == "__main__":
    test = Plan(3, 3)

    print(test)  # Affichage des points initiaux

    test.ajoutPoint(2, 3)

    print("\n",test)  # Affichage après ajout du nouveau point
    
    test.points[test.points.index()]