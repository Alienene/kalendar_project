from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
import json
from PyQt5.QtCore import QDate

class Widget(QMainWindow):
    def   __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.notes = {}
        self.ui.pushButton.clicked.connect(self.save_note)
        self.ui.calendarWidget.clicked.connect(self.show_note)
        self.ui.pushButton_2.clicked.connect(self.del_note)
        self.load_note()
        self.ui.lineEdit.textChanged.connect(self.search)
        self.ui.listWidget.itemClicked.connect(self.select_note)

    def show_note(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        note = self.notes.get(selected_date.toString(Qt.ISODate))
        self.ui.textEdit.setPlainText(note)

    def save_note(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        note_text = self.ui.textEdit.toPlainText()
        self.notes[selected_date.toString(Qt.ISODate)] = note_text
        self.upload_note()

    def del_note(self):
        selected_date = self.ui.calendarWidget.selectedDate()
        del self.notes[selected_date.toString(Qt.ISODate)]
        self.ui.textEdit.clear()
        self.upload_note()

    def upload_note(self):
        with open('notes.json','w') as file:
            json.dump(self.notes,file)
            QMessageBox.information(self,'Correct!','Save')

    def load_note(self):
        with open('notes.json','r') as file:
            self.notes = json.load(file)

    def search(self):
        t = self.ui.lineEdit.text().lower()
        filtered = {}
        for date, note in self.notes.items():
            if t in note:
                filtered[date] = note
        self.ui.listWidget.clear()
        for date, note in filtered.items():
            item = f"{date}:{note}"
            self.ui.listWidget.addItem(item)

    def select_note(self):
        d = self.ui.listWidget.currentItem().text().split(':')[0].strip()
        date = QDate.fromString(d, Qt.ISODate)
        self.ui.calendarWidget.setSelectedDate(date)
        self.show_note()

app = QApplication([])
ex = Widget()
ex.show()
app.exec_()
