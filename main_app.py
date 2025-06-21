import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableView, QMessageBox, QAbstractItemView, QHeaderView,
    QDialog 
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, Slot

import database
from item_dialog import ItemDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 CRUD Приложение 📝")
        self.setGeometry(100, 100, 700, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Таблица для отображения данных
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # Выделение всей строки
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Запрет прямого редактирования в таблице
        self.table_view.setAlternatingRowColors(True) # Чередование цветов строк

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['ID', 'Название', 'Описание'])
        self.table_view.setModel(self.model)

        # Настройка отображения столбцов
        self.table_view.setColumnHidden(0, True) # Скрыть столбец ID
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Растянуть столбец "Название"
        self.table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Растянуть столбец "Описание"


        self.layout.addWidget(self.table_view)

        # Контейнер для кнопок
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("➕ Добавить")
        self.add_button.clicked.connect(self.open_add_dialog)
        self.button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("✏️ Редактировать")
        self.edit_button.clicked.connect(self.open_edit_dialog)
        self.button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("❌ Удалить")
        self.delete_button.clicked.connect(self.delete_selected_item)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.load_data_into_table()

    def load_data_into_table(self):
        """Загружает данные из БД и отображает их в таблице."""
        self.model.removeRows(0, self.model.rowCount()) # Очистка таблицы перед загрузкой
        items = database.get_all_items()
        for item in items:
            row = [
                QStandardItem(str(item['id'])),
                QStandardItem(item['name']),
                QStandardItem(item['description'])
            ]
            # Делаем элементы нередактируемыми, если бы не было setEditTriggers
            for i in row:
                i.setEditable(False)
            self.model.appendRow(row)

    @Slot()
    def open_add_dialog(self):
        """Открывает диалог для добавления нового элемента."""
        dialog = ItemDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted: # Проверяем, была ли нажата "OK"
            name, description = dialog.get_data()
            if not name:
                QMessageBox.warning(self, "Ошибка ввода", "Название не может быть пустым.")
                return
            try:
                database.add_item(name, description)
                self.load_data_into_table()
                QMessageBox.information(self, "Успех", f"Элемент '{name}' успешно добавлен.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось добавить элемент: {e}")


    def get_selected_item_id_and_row(self):
        """Возвращает ID и индекс строки выбранного элемента, или None, None."""
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Ошибка выбора", "Пожалуйста, выберите элемент для выполнения операции.")
            return None, None
        selected_row_index = selected_indexes[0].row() # Берем первую выделенную строку
        item_id_item = self.model.item(selected_row_index, 0) # ID находится в первом столбце (скрытом)
        if item_id_item:
            return int(item_id_item.text()), selected_row_index
        return None, None


    @Slot()
    def open_edit_dialog(self):
        """Открывает диалог для редактирования выбранного элемента."""
        item_id, selected_row_index = self.get_selected_item_id_and_row()
        if item_id is None:
            return

        # Получаем текущие данные для предзаполнения диалога
        current_name_item = self.model.item(selected_row_index, 1)
        current_desc_item = self.model.item(selected_row_index, 2)

        current_name = current_name_item.text() if current_name_item else ""
        current_description = current_desc_item.text() if current_desc_item else ""

        dialog = ItemDialog(self, item_id=item_id, name=current_name, description=current_description)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name, new_description = dialog.get_data()
            if not new_name:
                QMessageBox.warning(self, "Ошибка ввода", "Название не может быть пустым.")
                return
            try:
                database.update_item(item_id, new_name, new_description)
                self.load_data_into_table()
                QMessageBox.information(self, "Успех", f"Элемент '{new_name}' успешно обновлен.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось обновить элемент: {e}")


    @Slot()
    def delete_selected_item(self):
        """Удаляет выбранный элемент после подтверждения."""
        item_id, selected_row_index = self.get_selected_item_id_and_row()
        if item_id is None:
            return

        item_name_item = self.model.item(selected_row_index, 1) # Имя для сообщения
        item_name = item_name_item.text() if item_name_item else "Выбранный элемент"

        reply = QMessageBox.question(self, "Подтверждение удаления",
                                     f"Вы уверены, что хотите удалить элемент '{item_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                database.delete_item(item_id)
                self.load_data_into_table() # Обновить таблицу
                QMessageBox.information(self, "Успех", f"Элемент '{item_name}' успешно удален.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось удалить элемент: {e}")


def main():
    app = QApplication()
    # database.initialize_database() # Убедимся, что БД и таблица созданы
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()