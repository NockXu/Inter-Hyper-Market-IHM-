# Classe permettant de savoir par où un objet est accessible d'un objet
class Accessibilite:
    def __init__(self, H: bool = True, B: bool = True, G: bool = True, D: bool = True) -> None:
        self._H = H
        self._B = B
        self._G = G
        self._D = D

    # Méthodes getters
    def get_H(self) -> bool:
        return self._H
    
    def get_B(self) -> bool:
        return self._B
    
    def get_G(self) -> bool:
        return self._G
    
    def get_D(self) -> bool:
        return self._D

    # Méthodes setters
    def set_H(self, H: bool) -> None:
        self._H = H
    
    def set_B(self, B: bool) -> None:
        self._B = B
    
    def set_G(self, G: bool) -> None:
        self._G = G
    
    def set_D(self, D: bool) -> None:
        self._D = D

    # Méthode spéciale __str__()
    def __str__(self) -> str:
        directions = []
        
        if self._H:
            directions.append("haut")
            
        if self._B:
            directions.append("bas")
            
        if self._G:
            directions.append("gauche")
            
        if self._D:
            directions.append("droite")
        
        if not directions:
            return "{None}"
        
        return "{" + ", ".join(directions) + "}"

    # Méthode spéciale __eq__()
    def __eq__(self, other) -> bool:
        if isinstance(other, Accessibilite):
            return (self._H == other._H) and (self._B == other._B) and \
                   (self._G == other._G) and (self._D == other._D)
        return False
    
if __name__ == "__main__":
    # Exemple d'utilisation
    accessibilite1 = Accessibilite(H=True, B=False, G=True, D=False)
    print(accessibilite1)  # Affiche : Accessibilité : haut gauche

    # Modifier les attributs
    accessibilite1.set_B(True)
    print(accessibilite1)  # Affiche : Accessibilité : haut bas gauche

    # Comparaison d'égalité
    accessibilite2 = Accessibilite(H=True, B=True, G=True, D=False)
    print("(accessibilite1 == accessibilite2) = ", accessibilite1 == accessibilite2)  # Affiche : False
