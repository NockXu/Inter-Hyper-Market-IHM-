from accessibilite import Accessibilite

class Fonction:
    def __init__(self, rayon : str = None, H : bool = True, B : bool = True, G : bool = True, D : bool = True):
        self.acces : Accessibilite = Accessibilite(H, B, G, D)
        self.rayon : str = rayon