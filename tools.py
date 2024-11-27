from PyQt5.QtGui import QColor


class BrushTool:
    def __init__(self, color, size):
        super(BrushTool, self).__init__()
        self.color = color
        self.size = size

    def set_color(self, color):
        self.color = color

    def set_size(self, size):
        self.size = size

    def get_as_dict(self):
        return {"size": self.size, "color": self.color}


class EraserTool:
    def __init__(self, size):
        super(EraserTool, self).__init__()
        self.size = size
        self.color = QColor(255, 255, 255)

    def set_size(self, size):
        self.size = size

    def get_as_dict(self):
        return {"size": self.size, "color": self.color}


class FigureTool:
    def __init__(self, name, color, outline_color):
        super(FigureTool, self).__init__()
        self.color = color
        self.outline_color = outline_color
        self.name = name

    def get_as_dict(self):
        return {
            "color": self.color,
            "outline_color": self.outline_color,
        }


class SelectionTool:
    def __init__(self):
        pass
