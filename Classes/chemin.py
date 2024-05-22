import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.fonction import Fonction

class Chemin(Fonction):
    def __init__(self):
        super().__init__("chemin")