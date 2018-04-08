import logging
import os
import pandas as pd

from glob import glob
from collections import Counter
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

from .view import BinaryClassifierViewer


LOGGER = logging.getLogger(__name__)


class BinaryClassifierApp(BinaryClassifierViewer):
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
        if self.image_index == len(self.image_paths) - 1:
            QMessageBox.information(self, 'Information', 'Reach the end of images')
        self.image_label[self.image_paths[self.image_index]] = 0
        self.image_index = min(self.image_index+1, len(self.image_paths) - 1)
        self._render_image()

    @pyqtSlot()
    def _on_click_right(self):
        if self.image_index == len(self.image_paths) - 1:
            QMessageBox.information(self, 'Information', 'Reach the end of images')
        self.image_label[self.image_paths[self.image_index]] = 1
        self.image_index = min(self.image_index+1, len(self.image_paths) - 1)
        self._render_image()

    @pyqtSlot()
    def _export(self):
        orderdict = OrderedDict(sorted(self.image_label.items(), key=lambda x: x[0]))
        outfile = os.path.join(self.outdir, 'results.csv')
        df = pd.DataFrame(data={'image': list(orderdict.keys()), 'label': list(orderdict.values())}, dtype='uint8')
        df.to_csv(outfile, index=False)
        LOGGER.info('Export label result {}'.format(outfile))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            self.btn_false.click()
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            self.btn_true.click()
        else:
            LOGGER.warn('You Clicked {} but nothing happened...'.format(event.key()))
