from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel
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

        self.setLayout(layout)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    coffee_app = CoffeeApp()
    coffee_app.show()
    sys.exit(app.exec_())
