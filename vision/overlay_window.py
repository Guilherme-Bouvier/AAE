import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class OverlayWindow(QtWidgets.QWidget):

    region_selected = None

    def __init__(self):

        super().__init__()

        self.setWindowTitle("AAE Overlay Sensor")

        # janela sem borda
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )

        # transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.start = None
        self.end = None

        self.rect = None

        self.setGeometry(200, 200, 400, 300)

        self.show()

    # ============================
    # MOUSE PRESS
    # ============================

    def mousePressEvent(self, event):

        self.start = event.pos()
        self.end = self.start

        self.update()

    # ============================
    # MOUSE MOVE
    # ============================

    def mouseMoveEvent(self, event):

        self.end = event.pos()
        self.update()

    # ============================
    # MOUSE RELEASE
    # ============================

    def mouseReleaseEvent(self, event):

        self.end = event.pos()

        x1 = min(self.start.x(), self.end.x())
        y1 = min(self.start.y(), self.end.y())
        x2 = max(self.start.x(), self.end.x())
        y2 = max(self.start.y(), self.end.y())

        self.region_selected = {
            "left": self.x() + x1,
            "top": self.y() + y1,
            "width": x2 - x1,
            "height": y2 - y1
        }

        print("REGIÃO SELECIONADA:", self.region_selected)

        self.close()

    # ============================
    # PAINT (DESENHO VISUAL)
    # ============================

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)

        painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0), 2))

        if self.start and self.end:

            rect = QtCore.QRect(self.start, self.end)
            painter.drawRect(rect)


# ============================
# EXECUÇÃO
# ============================

def run_overlay():

    app = QtWidgets.QApplication(sys.argv)

    window = OverlayWindow()

    app.exec_()

    return window.region_selected