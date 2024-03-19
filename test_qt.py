import sys
import csv
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from itertools import cycle
from datetime import datetime
from design import Ui_MainWindow
import matplotlib.pyplot as plt

with open('expenses.csv', newline='\n') as csvfile:
    expenses = csv.reader(csvfile, delimiter=',', quotechar='|')
    expenses = list(expenses)
    title_expenses = expenses[0]
    main_expenses = expenses[1:]

    res_numbers = [float(i[-1]) for i in main_expenses]
    maxx = max(res_numbers)
    minn = min(res_numbers)
    average = sum(res_numbers) / len(res_numbers)
    licycle = cycle(main_expenses)


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.set_widget)
        self.pushButton_3.clicked.connect(self.create_pie)
        self.pushButton_4.clicked.connect(self.create_plot)
        self.pushButton_5.clicked.connect(self.calculate)
        self.item_list = []
        self.model_1 = QtCore.QStringListModel(self)

    def create_plot(self):
        dates = list(map(lambda x: datetime.strptime(x, '%Y-%m-%d'), [i[0] for i in main_expenses]))
        costs = [float(i[-1]) for i in main_expenses]
        dictionary = {}
        for i, k in enumerate(dates):
            if k not in dictionary:
                dictionary[k] = costs[i]
            else:
                dictionary[k] += costs[i]
        sorted_dict = dict(sorted(dictionary.items()))
        plt.plot(sorted_dict.keys(), sorted_dict.values(), linewidth=3)
        plt.savefig('2.png', dpi=70)
        pixmap2 = QPixmap('2.png')
        plt.close()
        self.label.setPixmap(pixmap2)
        self.label.resize(pixmap2.width(), pixmap2.height())

    def create_pie(self):
        dictt = {}
        for i in main_expenses:
            if i[1] not in dictt:
                dictt[i[1]] = float(i[-1])
            else:
                dictt[i[1]] += float(i[-1])

        labels = dictt.keys()
        sizes = dictt.values()
        fig, ax = plt.subplots()
        ax.pie(sizes,  labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.savefig('1.png', dpi=70)
        plt.close()
        pixmap = QPixmap('1.png')
        self.label_2.setPixmap(pixmap)
        self.label_2.resize(pixmap.width(), pixmap.height())

    def calculate(self):
        if self.buttonGroup.checkedButton().text() == "Минимум":
            self.lcdNumber.display(minn)
        elif self.buttonGroup.checkedButton().text() == "Максимум":
            self.lcdNumber.display(maxx)
        else:
            self.lcdNumber.display(average)

    def set_widget(self):
        self.listWidget.addItem(" ".join(next(licycle)))

    def run(self):
        self.item_list = [" ".join(i) for i in main_expenses]
        self.model_1.setStringList(self.item_list)
        self.listView.setModel(self.model_1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())