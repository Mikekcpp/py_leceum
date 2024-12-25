from PyQt5.QtWidgets import QDialog, QColorDialog
from PyQt5 import uic


class BrushSettingsDialog(QDialog):
    def __init__(self, mouse_pos, current_settings):
        super().__init__()
        uic.loadUi("brush_settings_dialog.ui", self)
        self.move(mouse_pos)

        self.spin_brush_size.setValue(current_settings.get("size"))
        self.btn_brush_color.setStyleSheet(
            f'background-color: {current_settings.get("color").name()}'
        )
        self.btn_brush_color.setText(current_settings.get("color").name())

        self.color = current_settings.get("color")

        self.btn_brush_color.clicked.connect(self.select_color)
        self.btn_apply.clicked.connect(self.close)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            self.btn_brush_color.setStyleSheet(f"background-color: {color.name()};")
            self.btn_brush_color.setText(color.name())

    def get_settings(self):
        return {
            "color": self.color if self.color else None,
            "size": self.spin_brush_size.value(),
        }