from chemin import Chemin

class Entrer(Chemin):
    def __init__(self, nom : str = None):
        super().__init__()
        self.nom = nom