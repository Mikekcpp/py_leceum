from query_db import *
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem


class FilesHistoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("files_history.ui", self)
        self.fill_table()

        self.btn_open.clicked.connect(self.open)

        self.selected_file_path = None

    def open(self):
        selected_row_index = self.tbl_history.currentRow()

        if selected_row_index is not None:
            row = [
                self.tbl_history.item(selected_row_index, i).text()
                for i in range(self.tbl_history.columnCount())
            ]

            self.selected_file_path = row[2]
            self.close()

    def get_selected_file(self):
        return self.selected_file_path

    def fill_table(self):
        history = get_history()
        for i, row in enumerate(history):
            self.tbl_history.setRowCount(self.tbl_history.rowCount() + 1)
            row = row[1:]
            for j, el in enumerate(row):
                self.tbl_history.setItem(i, j, QTableWidgetItem(str(el)))

        self.tbl_history.resizeColumnsToContents()
