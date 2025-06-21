from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QDialogButtonBox, QLabel
)

class ItemDialog(QDialog):
    def __init__(self, parent=None, item_id=None, name="", description=""):
        super().__init__(parent)

        self.item_id = item_id
        if self.item_id:
            self.setWindowTitle("Редактировать элемент")
        else:
            self.setWindowTitle("Добавить элемент")

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.name_label = QLabel("Название:")
        self.name_input = QLineEdit(name)
        self.name_input.setPlaceholderText("Введите название элемента")
        self.form_layout.addRow(self.name_label, self.name_input)

        self.desc_label = QLabel("Описание:")
        self.desc_input = QLineEdit(description)
        self.desc_input.setPlaceholderText("Введите описание (необязательно)")
        self.form_layout.addRow(self.desc_label, self.desc_input)

        self.layout.addLayout(self.form_layout)

        # Стандартные кнопки OK и Cancel
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept) # Сигнал для закрытия с QDialog.Accepted
        self.button_box.rejected.connect(self.reject) # Сигнал для закрытия с QDialog.Rejected

        self.layout.addWidget(self.button_box)
        self.setMinimumWidth(300)


    def get_data(self):
        """Возвращает введенные данные из полей диалога."""
        return self.name_input.text().strip(), self.desc_input.text().strip()