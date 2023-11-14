import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = True
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Календарь для заметок')
        self.setGeometry(300, 300, 1920, 1080)

        self.event = QLineEdit(self)  # запись события
        self.event.move(1250, 5)
        self.event.resize(500, 35)
        font = QFont('Times', 12)
        self.event.setStyleSheet('border: 1px solid black')
        self.event.setFont(font)

        self.result = QListWidget(self)  # Список заметок
        self.result.resize(500, 500)
        self.result.move(1250, 100)
        font2 = QFont('Times', 12)
        self.result.setStyleSheet('border: 1px solid black')
        self.result.setFont(font2)

        self.lbl = QLabel('Поле для ввода заметок:', self)  # Надпись 1
        self.lbl.move(1000, 0)
        self.lbl.setFont(QFont('Times', 16))

        self.lbl2 = QLabel('Ваши заметки:', self)  # Надпись 2
        self.lbl2.move(1100, 100)
        self.lbl2.setFont((QFont('Times', 16)))

        self.btn = QPushButton('Добавить в заметки',
                               self)  # Кнопка добавления в заметки
        self.btn.move(1755, 5)
        self.btn.setFont(QFont('Times', 12))
        self.btn.resize(160, 35)
        self.btn.setStyleSheet('border: 1px solid black; color: red')
        self.btn.clicked.connect(self.addItem)

        self.buttonSave = QPushButton('Сохранить',
                                      self)  # Кнопка сохранения файла
        self.buttonSave.move(1750, 975)
        self.buttonSave.setFont(QFont('Times', 12))
        self.buttonSave.resize(160, 35)
        self.buttonSave.setStyleSheet('border: 1px solid black; color: red')
        self.buttonSave.clicked.connect(self.savelst)

        self.buttonClear = QPushButton('Очистить',
                                       self)  # Кнопка очистки списка
        self.buttonClear.move(1450, 975)
        self.buttonClear.setFont(QFont('Times', 12))
        self.buttonClear.resize(160, 35)
        self.buttonClear.setStyleSheet('border: 1px solid black; color: red')
        self.buttonClear.clicked.connect(self.clearlst)

        self.real_btn = QPushButton('Сегодняшнее число',
                                    self)  # Кнопка возвращающая на сегодняшнее число
        self.real_btn.move(1150, 975)
        self.real_btn.setFont(QFont('Times', 12))
        self.real_btn.resize(160, 35)
        self.real_btn.setStyleSheet('border: 1px solid black; color: red')
        self.real_btn.clicked.connect(self.day_today)

        self.UiComponents()
        self.show()

    def addItem(self):
        date = self.calendar.selectedDate().toString(
            "dd.MM.yyyy")  # Добавить элемент в список с датой
        text = self.event.text()
        items = f"{date}: {text}"
        self.result.addItem(items)
        self.event.clear()

    def select_item(self, date):
        for i in range(
                self.result.count()):  # Функция, показывающая при нажатии на дату, заметку
            item = self.result.item(i)
            stroke = item.text()
            if stroke.startswith(date.toString("dd.MM.yyyy")):
                self.result.setCurrentItem(item)
                return

    def day_today(self):
        today = QDate.currentDate()  # Функция, перемещающая на нынешний день
        self.calendar.setSelectedDate(today)

    def closeEvent(self, event):  # Диалоговое окно
        request = QMessageBox.question(self, 'Подтверждение',
                                       "Вы действительно хотите выйти?",
                                       QMessageBox.Yes |
                                       QMessageBox.No, QMessageBox.No)

        if request == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def savelst(self):  # Функция, сохраняющая в файл
        name, _ = QFileDialog.getSaveFileName(self, "Save List", "",
                                              "Text Files (*.txt);;All Files (*)")  # выбор, в каком формате файла сохранить
        if name:
            with open(name, 'w') as f:
                for i in range(self.result.count()):
                    item = self.result.item(i)
                    f.write(item.text() + '\n')

    def show_date(self,
                  it_m):  # Функция, при нажатии на заметку, показывается дата
        dates = it_m.text()
        d_str = dates.split(':')[0]
        date_2 = QDate.fromString(d_str, "dd.MM.yyyy")  # специальная форма записи даты в QCalendarWidget
        self.calendar.setSelectedDate(date_2)

    def clearlst(self):  # Функция, очистки списка заметок
        self.result.clear()

    def edit_item(self, item):  # Функция по редактированию заметок
        text = item.text()
        n_t, ok_pressed = QInputDialog.getText(self, "Редактировать заметку",
                                               "Введите новый текст:",
                                               QLineEdit.Normal,
                                               text)
        if ok_pressed and n_t:
            item.setText(n_t)

    def UiComponents(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setFont(QFont('Times', 12))
        self.calendar.setGeometry(0, 0, 1000, 1030)
        self.calendar.setStyleSheet('background: PaleTurquoise')
        self.calendar.repaint()
        self.result.itemClicked.connect(
            self.show_date)  # Функция, при нажатии на заметку, показывается дата
        self.calendar.selectionChanged.connect(lambda: self.select_item(
            self.calendar.selectedDate()))  # Обрабатывает событие, когда нажимают дату, выбирается нужная заметка
        self.result.itemDoubleClicked.connect(
            self.edit_item)  # Двойной щелчок, для активации редактирования заметки


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calendar = Calendar()
    calendar.show()
    sys.exit(app.exec_())
