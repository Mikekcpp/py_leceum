from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)
from PyQt5 import uic
import sqlite3, sys


class CoffeeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.display_coffee_info()

    def initUI(self):
        self.setWindowTitle("Информация о кофе")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Информация о кофе:")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.add_button = QPushButton("Добавить кофе")
        self.add_button.clicked.connect(self.open_add_edit_form)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.display_coffee_info()

    def fetch_coffee_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        data = cursor.fetchall()
        conn.close()
        return data

    def display_coffee_info(self):
        coffee_data = self.fetch_coffee_data()
        self.text_edit.clear()
        for coffee in coffee_data:
            info = f"ID: {coffee[0]}, Название: {coffee[1]}, Обжарка: {coffee[2]}, Тип: {coffee[3]}, Вкус: {coffee[4]}, Цена: {coffee[5]}, Объем: {coffee[6]}"
            self.text_edit.append(info)

    def open_add_edit_form(self, coffee_id=None):
        self.form = AddEditCoffeeForm(coffee_id)
        self.form.saved.connect(self.display_coffee_info)
        self.form.show()


class AddEditCoffeeForm(QWidget):
    saved = pyqtSignal()

    def __init__(self, coffee_id=None):
        super().__init__()
        self.coffee_id = coffee_id
        self.initUI()

        if coffee_id:
            self.load_coffee_data(coffee_id)

    def initUI(self):
        self.setWindowTitle("Добавить/Редактировать кофе")
        self.setGeometry(100, 100, 300, 250)

        layout = QGridLayout()

        layout.addWidget(QLabel("Название:"), 0, 0)
        self.lineEditName = QLineEdit()
        layout.addWidget(self.lineEditName, 0, 1)

        layout.addWidget(QLabel("Обжарка:"), 1, 0)
        self.lineEditRoast = QLineEdit()
        layout.addWidget(self.lineEditRoast, 1, 1)

        layout.addWidget(QLabel("Тип:"), 2, 0)
        self.lineEditType = QLineEdit()
        layout.addWidget(self.lineEditType, 2, 1)

        layout.addWidget(QLabel("Вкус:"), 3, 0)
        self.lineEditFlavor = QLineEdit()
        layout.addWidget(self.lineEditFlavor, 3, 1)

        layout.addWidget(QLabel("Цена:"), 4, 0)
        self.lineEditPrice = QLineEdit()
        layout.addWidget(self.lineEditPrice, 4, 1)

        layout.addWidget(QLabel("Объем:"), 5, 0)
        self.lineEditVolume = QLineEdit()
        layout.addWidget(self.lineEditVolume, 5, 1)

        self.pushButtonSave = QPushButton("Сохранить")
        self.pushButtonSave.clicked.connect(self.save_coffee_data)
        layout.addWidget(self.pushButtonSave, 6, 0)

        self.pushButtonCancel = QPushButton("Отмена")
        self.pushButtonCancel.clicked.connect(self.close)
        layout.addWidget(self.pushButtonCancel, 6, 1)

        self.setLayout(layout)

    def load_coffee_data(self, coffee_id):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id=?", (coffee_id,))
        coffee = cursor.fetchone()
        conn.close()
        if coffee:
            self.lineEditName.setText(coffee[1])
            self.lineEditRoast.setText(coffee[2])
            self.lineEditType.setText(coffee[3])
            self.lineEditFlavor.setText(coffee[4])
            self.lineEditPrice.setText(str(coffee[5]))
            self.lineEditVolume.setText(str(coffee[6]))

    def save_coffee_data(self):
        name = self.lineEditName.text()
        roast = self.lineEditRoast.text()
        coffee_type = self.lineEditType.text()
        flavor = self.lineEditFlavor.text()
        price = self.lineEditPrice.text()
        volume = self.lineEditVolume.text()

        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()

        if self.coffee_id:
            cursor.execute(
                "UPDATE coffee SET name=?, roast=?, type=?, flavor=?, price=?, volume=? WHERE id=?",
                (name, roast, coffee_type, flavor, price, volume, self.coffee_id),
            )
        else:
            cursor.execute(
                "INSERT INTO coffee (name, roast, type, flavor, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast, coffee_type, flavor, price, volume),
            )

        conn.commit()
        conn.close()
        self.saved.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CoffeeApp()
    main_window.show()
    sys.exit(app.exec_())
