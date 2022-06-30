from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


# Credits to:
# https://stackoverflow.com/questions/10533838/displaying-a-standard-icon-and-text-in-qlabel
class QIconLabel(QWidget):
    def __init__(self, icon, text, size=64, hSpacing=10, parent=None, final_stretch=True):
        super().__init__(parent)
        # self.setObjectName("QIconLabel")  # TODO
        self.iconSize = QSize(size, size)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.iconLabel = QLabel()
        iconPixmap = icon.pixmap(self.iconSize)
        self.iconLabel.setPixmap(iconPixmap)
        self.iconLabel.setObjectName("iconLabel")

        layout.addWidget(self.iconLabel)
        layout.addSpacing(hSpacing)
        self.textLabel = QLabel(text)
        self.textLabel.setObjectName("textLabel")
        layout.addWidget(self.textLabel)
        self.textLabel.setAlignment(Qt.AlignCenter);

        if final_stretch:
            layout.addStretch()
    
    def setText(self, text):
        self.textLabel.setText(text)
