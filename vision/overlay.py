import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor


class Overlay(QWidget):

    def __init__(self):
        super().__init__()

        # 🔥 janela sem borda
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        # 🔥 fundo transparente
        self.setAttribute(Qt.WA_TranslucentBackground)

        # tamanho inicial do "sensor"
        self.setGeometry(300, 300, 300, 200)

        self.dragging = False
        self.offset = None

        self.label = QLabel("📡 AAE SENSOR", self)
        self.label.setStyleSheet("color: red; font-size: 14px;")
        self.label.move(10, 10)

        self.show()

    # ============================
    # DESENHO DA ÁREA
    # ============================

    def paintEvent(self, event):

        painter = QPainter(self)

        # 🔥 borda do sensor
        painter.setPen(QColor(255, 0, 0))
        painter.drawRect(self.rect())

        # 🔥 leve transparência interna
        painter.setBrush(QColor(255, 0, 0, 30))
        painter.drawRect(self.rect())

    # ============================
    # MOVER JANELA
    # ============================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):

        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    # ============================
    # REDIMENSIONAR (simples)
    # ============================

    def keyPressEvent(self, event):

        # aumentar área
        if event.key() == Qt.Key_Up:
            self.resize(self.width(), self.height() + 10)

        # diminuir área
        if event.key() == Qt.Key_Down:
            self.resize(self.width(), max(50, self.height() - 10))

        # largura +
        if event.key() == Qt.Key_Right:
            self.resize(self.width() + 10, self.height())

        # largura -
        if event.key() == Qt.Key_Left:
            self.resize(max(50, self.width() - 10), self.height())


# ============================
# EXECUÇÃO
# ============================

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Overlay()
    sys.exit(app.exec_())