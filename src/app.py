import logging
import os
import pandas as pd

from glob import glob

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

from view import BinaryClassifierViewer


LOGGER = logging.getLogger(__name__)


class BinaryClassifierApp(BinaryClassifierViewer, QMainWindow):
    def __init__(self, imgdir):
        super().__init__()
        self.image_paths = glob(os.path.abspath(imgdir))
        self.image_index = 0
        self.true_images = []
        self.false_images = []
        self.btn_false.clicked.connect(self._on_click_left)
        self.btn_true.clicked.connect(self._on_click_right)
        self._render_image()

    def _render_image(self):
        assert 0 <= self.image_index < len(self.image_paths)
        image = QPixmap(self.image_paths[self.image_index])
        self.label_head.setPixmap(image)
        self._render_status()
        self.show()

    def _render_status(self):
        image_name = os.path.basename(self.image_paths[self.image_index])
        self.label_status.setText('({}/{}) {}'.format(self.image_index + 1, len(self.image_paths), image_name))
        self.btn_false.setText('< False ({})'.format(len(self.false_images)))
        self.btn_true.setText('True ({}) >'.format(len(self.true_images)))
        pass

    @pyqtSlot()
    def _on_click_left(self):
        print('false')
        self.false_images.append(self.image_paths[self.image_index])
        self.image_index += 1
        self._render_image()

    @pyqtSlot()
    def _on_click_right(self):
        print('true')
        self.true_images.append(self.image_paths[self.image_index])
        self.image_index += 1
        self._render_image()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            self.btn_false.click()
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            self.btn_true.click()
        else:
            print('You Clicked {} but nothing happened...'.format(event.key()))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    classifier = BinaryClassifierApp('/home/afun/Desktop/UNet_result/*')
    app.exec()
