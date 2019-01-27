import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore
from PyQt5 import uic

from PIL import Image
from PIL.ImageQt import ImageQt

import ImageToMap


class MapperGui(QMainWindow):

    def __init__(self):
        super().__init__()

        self.template_image = None
        self.colors_image = None


        self.resize(1280, 800)
        self.setStyleSheet("background-color:white;")
        uic.loadUi('mainwindow.ui', self)

        # Center the screen
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        self._set_up_image_drops()

        self.calculateButton.pressed.connect(self.calculate_final_image)
        self.showFullImageButton.pressed.connect(self.show_full_image)
        self.saveAsButton.pressed.connect(self.save_as)

        self.show()

    def _set_up_image_drops(self):
        self.colorsImageDrop.setAcceptDrops(True)
        self.templateImageDrop.setAcceptDrops(True)

        def check_drag_event(e):
            file_name = e.mimeData().urls()[0].toLocalFile()
            try:
                Image.open(file_name)
                e.accept()
            except OSError as e:
                pass

        def colors_drop_event(e):
            self.load_colors_image(e.mimeData().urls()[0].toLocalFile())

        def template_drop_event(e):
            self.load_template_image(e.mimeData().urls()[0].toLocalFile())


        self.colorsImageDrop.dragEnterEvent = check_drag_event
        self.colorsImageDrop.dropEvent = colors_drop_event

        self.templateImageDrop.dragEnterEvent = check_drag_event
        self.templateImageDrop.dropEvent = template_drop_event

    def load_template_image(self, image_location):
        self.template_image = Image.open(image_location)

        pixmap = QPixmap(image_location)
        if pixmap is None:
            return

        # Scale the image down to fit in the label
        pixmap = pixmap.scaled(self.templateImageDrop.width(), self.templateImageDrop.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)


        self.templateImageDrop.setPixmap(pixmap)
        self.templateImageDrop.show()

    def load_colors_image(self, image_location):
        self.colors_image = Image.open(image_location)
        pixmap = QPixmap(image_location)
        if pixmap is None:
            return

        # Scale the image down to fit in the label
        pixmap = pixmap.scaled(self.colorsImageDrop.width(), self.colorsImageDrop.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)


        self.colorsImageDrop.setPixmap(pixmap)
        self.colorsImageDrop.show()

    def refresh_final_image_view(self):
        qtImage = ImageQt(self.final_image)
        pixmap = QPixmap.fromImage(qtImage)
        if pixmap is None:
            return

        # Scale the image down to fit in the label
        pixmap = pixmap.scaled(self.finalImageView.width(), self.finalImageView.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)


        self.finalImageView.setPixmap(pixmap)

    def calculate_final_image(self):
        if self.colors_image is None or self.template_image is None:
            return

        self.final_image = ImageToMap.map_image(self.colors_image, self.template_image)
        self.refresh_final_image_view()

    def save_as(self):
        if self.final_image is None:
            return

        file_location = QFileDialog.getSaveFileName(self, 'Save File')
        if file_location[0] == '':
            return

        self.final_image.save(file_location[0])

    def show_full_image(self):
        if self.final_image is None:
            return
        self.final_image.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MapperGui()

    sys.exit(app.exec())