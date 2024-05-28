# Programme réaliser par Monsieur Cozot et modifier pour coller à la demande de la SAE
# Le programme à pour but d'afficher une image venant de google


from http.client import responses
from typing_extensions import Self
import requests
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QResizeEvent
from PyQt6.QtCore import Qt


#import random

class WImage(QLabel):
    def __init__(self):
        super().__init__()

        self.minSize = 400
        self.pixmax = QPixmap(self.minSize, self.minSize)
        self.setPixmap(self.pixmax)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def query(self, image: str) -> None:
        r = requests.get("https://api.qwant.com/v3/search/images",
                         params={
                             'count': 50,
                             'q': image,
                             't': 'images',
                             'safesearch': 1,
                             'locale': 'en_US',
                             'offset': 0,
                             'device': 'desktop'
                         },
                         headers={
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                         }
                         )

        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]

        pixmap = QPixmap()

        for url in urls:
            response = requests.get(url)
            pixmap.loadFromData(response.content)

            if not pixmap.isNull():
                break

        w = min(pixmap.width(), self.minSize)
        h = min(pixmap.height(), self.minSize)
        self.pixmax = pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        self.setPixmap(self.pixmax.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def resizeEvent(self, event):
        pixmap = self.pixmax
        pixmap = pixmap.scaled(event.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        self.setPixmap(pixmap)