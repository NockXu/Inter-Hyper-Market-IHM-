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
                             'count': 10,  # Augmenter le nombre d'images pour avoir plus d'options
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
        if not response:
            return

        urls = [item.get('media') for item in response if item.get('media')]

        for url in urls:
            head_response = requests.head(url)
            content_length = head_response.headers.get('Content-Length')

            # Prioritize smaller images by setting a threshold (e.g., 1 MB)
            if content_length and int(content_length) < 1024 * 1024:
                image_response = requests.get(url)
                pixmap = QPixmap()
                pixmap.loadFromData(image_response.content)

                if not pixmap.isNull():
                    w = min(pixmap.width(), self.minSize)
                    h = min(pixmap.height(), self.minSize)
                    self.pixmax = pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
                    self.setPixmap(self.pixmax.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))
                    self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                    break

    def resizeEvent(self, event):
        pixmap = self.pixmax
        pixmap = pixmap.scaled(event.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        self.setPixmap(pixmap)