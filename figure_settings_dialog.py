from PyQt5.QtWidgets import QDialog, QColorDialog
from PyQt5 import uic


class FigureSettingsDialog(QDialog):
    def __init__(self, mouse_pos, current_settings):
        super().__init__()
        uic.loadUi("figure_settings_dialog.ui", self)
        self.move(mouse_pos)

        self.color = current_settings.get("color")
        self.outline_color = current_settings.get("outline_color")

        self.style_button(self.btn_figure_color, self.color)
        self.style_button(self.btn_figure_outline_color, self.outline_color)

        self.btn_apply.clicked.connect(self.close)
        self.btn_figure_color.clicked.connect(self.get_color)
        self.btn_figure_outline_color.clicked.connect(self.get_outline_color)

    @staticmethod
    def style_button(btn, color):
        btn.setText(color.name())
        btn.setStyleSheet(f"background-color: {color.name()}")

    def get_color(self):
        self.color = QColorDialog.getColor()
        if self.color.isValid():
            self.style_button(self.btn_figure_color, self.color)

    def get_outline_color(self):
        self.outline_color = QColorDialog.getColor()
        if self.outline_color.isValid():
            self.style_button(self.btn_figure_outline_color, self.outline_color)

    def get_settings(self):
        return {
            "color": self.color,
            "outline_color": self.outline_color,
        }
