import logging
import os
import pandas as pd

from glob import glob
from collections import Counter

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

from .view import BinaryClassifierViewer


LOGGER = logging.getLogger(__name__)


class BinaryClassifierApp(BinaryClassifierViewer, QMainWindow):
    def __init__(self, imgdir, outdir):
        super().__init__()
        self.outdir = outdir
        self.image_paths = glob(os.path.abspath(imgdir))
        self.image_index = 0
        self.image_label = {img: None for img in self.image_paths}
        self.btn_false.clicked.connect(self._on_click_left)
        self.btn_true.clicked.connect(self._on_click_right)
        self.btn_confirm.clicked.connect(self._export)
        self._render_image()

    def _render_image(self):
        assert 0 <= self.image_index < len(self.image_paths)
        image = QPixmap(self.image_paths[self.image_index])
        self.label_head.setPixmap(image)
        self._render_status()
        self.show()

    def _render_status(self):
        image_name = os.path.basename(self.image_paths[self.image_index])
        counter = Counter(self.image_label.values())
        self.label_status.setText('({}/{}) {}'.format(self.image_index + 1, len(self.image_paths), image_name))
        self.btn_false.setText('< False ({})'.format(counter[0]))
        self.btn_true.setText('True ({}) >'.format(counter[1]))

    @pyqtSlot()
    def _on_click_left(self):
        self.image_label[self.image_paths[self.image_index]] = 0
        self.image_index += 1
        self._render_image()

    @pyqtSlot()
    def _on_click_right(self):
        self.image_label[self.image_paths[self.image_index]] = 1
        self.image_index += 1
        self._render_image()

    @pyqtSlot()
    def _export(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            self.btn_false.click()
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            self.btn_true.click()
        else:
            LOGGER.info('You Clicked {} but nothing happened...'.format(event.key()))
