from PyQt5.QtWidgets import QDialog, QColorDialog
from PyQt5 import uic


class EraserSettingsDialog(QDialog):
    def __init__(self, mouse_pos, current_settings):
        super().__init__()
        uic.loadUi("eraser_settings_dialog.ui", self)
        self.move(mouse_pos)

        self.spin_brush_size.setValue(current_settings.get("size"))
        self.btn_apply.clicked.connect(self.close)

    def get_settings(self):
        return {
            "size": self.spin_brush_size.value(),
        }
