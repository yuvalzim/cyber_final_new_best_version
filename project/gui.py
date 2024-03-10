from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import update_DB
import options_comp
from consts import *
from options_comp import Ui_Form


class Ui_MainWindow(QtWidgets.QWidget):

    def setupUi(self, MainWindow, num_of_comps, comp_dict):
        self.is_sub_wnd_open = False
        self.comp_dict = comp_dict
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comp_arr = []
        self.x_image = X_DRAW_START
        self.y_image = Y_DRAW_START
        self.row_count = 0
        self.current_page = 1
        self.headline_start_x = 330
        self.headline_start_y = -10
        self.scan_x = 890
        self.scan_y = 720
        self.scroll_diff = 0
        self.num_of_comps = num_of_comps
        self.images = []
        self.keys_list = list(self.comp_dict.keys())
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1093, 892)

        self.centralwidget = QtWidgets.QMainWindow()
        self.centralwidget.setObjectName("centralwidget")

        self.headline = QtWidgets.QLabel(self.centralwidget)
        self.headline.setGeometry(QtCore.QRect(self.headline_start_x, self.headline_start_y, 441, 191))
        font = QtGui.QFont()
        font.setPointSize(28)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.headline.setFont(font)
        self.headline.setAutoFillBackground(False)
        self.headline.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.headline.setFrameShadow(QtWidgets.QFrame.Plain)
        self.headline.setLineWidth(1)
        self.headline.setScaledContents(False)
        self.headline.setAlignment(QtCore.Qt.AlignCenter)
        self.headline.setWordWrap(False)
        self.headline.setObjectName("headline")

        MainWindow.setCentralWidget(self.centralwidget)

        self.LeftArrow = QtWidgets.QToolButton(self.centralwidget)
        self.LeftArrow.setGeometry(QtCore.QRect(400, 780, 91, 61))
        self.LeftArrow.setArrowType(QtCore.Qt.LeftArrow)
        self.LeftArrow.setObjectName("toolButton")

        self.RightArrow = QtWidgets.QToolButton(self.centralwidget)
        self.RightArrow.setGeometry(QtCore.QRect(570, 780, 91, 61))
        self.RightArrow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.RightArrow.setArrowType(QtCore.Qt.RightArrow)
        self.RightArrow.setObjectName("toolButton_2")

        self.page_num = QtWidgets.QLabel(self.centralwidget)
        self.page_num.setGeometry(QtCore.QRect(500, 740, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.page_num.setFont(font)
        self.page_num.setAlignment(QtCore.Qt.AlignCenter)
        self.page_num.setObjectName("page_num")

        self.scan_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_button.setGeometry(QtCore.QRect(self.scan_x, self.scan_y, 141, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.scan_button.setFont(font)
        self.scan_button.setObjectName("pushButton")

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Check for clicks
        current_num = self.num_of_comps
        if self.num_of_comps > 6:
            current_num = 6

        for i in range(current_num):
            self.draw_computer(i)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # for i in range(current_num):
        #     current_button_index = (self.current_page - 1) * 6 + i
        #     self.comp_arr[current_button_index].clicked.connect(
        #         lambda: self.select_comp(self.comp_arr[current_button_index]))

        print(1)
        self.LeftArrow.clicked.connect(lambda: self.left_page(MainWindow))
        self.RightArrow.clicked.connect(lambda: self.right_page(MainWindow))
        self.scan_button.clicked.connect(lambda: self.scan(MainWindow))
        print(2)

    def draw_computer(self, i):
        image = self.get_correct_pic(i)
        keys_list = list(self.comp_dict.keys())
        self.row_count += 1

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(self.x_image, self.y_image, 171, 171))
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap(image))
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.images.append(self.image)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.select = QtWidgets.QPushButton(self.centralwidget)
        self.select.setGeometry(QtCore.QRect(self.x_image + 14, self.y_image + 180, 150, 41))
        self.select.setObjectName(f"Select{i}")
        self.select.setText(keys_list[i])
        self.select.setFont(font)
        self.comp_arr.append(self.select)

        self.select.clicked.connect(lambda: self.select_comp(self.comp_arr[i]))

        self.x_image += 380
        if self.row_count == 3:
            self.row_count = 0
            self.y_image += 300
            self.x_image = X_DRAW_START

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.headline.setText(_translate("MainWindow", "Antivirus"))
        self.LeftArrow.setText(_translate("MainWindow", "..."))
        self.RightArrow.setText(_translate("MainWindow", "..."))
        self.page_num.setText(_translate("MainWindow", "1"))
        self.scan_button.setText(_translate("MainWindow", "Scan"))

    def select_comp(self, button):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window, button.text())
        self.window.show()

    def get_correct_pic(self, index):
        if list(self.comp_dict.values())[int(index)] == 1:
            image = "on_monitor.png"
        else:
            image = "off_monitor.png"
        return image

    def erase_win(self):
        for i in range(len(self.images)):
            self.images[i].setVisible(False)
            self.comp_arr[i].setVisible(False)

    def right_page(self, MainWindow):
        if self.num_of_comps > 6:
            self.erase_win()
            self.current_page += 1
            self.num_of_comps -= 6
            self.row_count = 0
            self.page_num.setText(str(self.current_page))
            for i in range(min(self.num_of_comps, 6)):
                self.images[i].setVisible(True)
                self.comp_arr[i].setVisible(True)
                self.images[i].setPixmap(QtGui.QPixmap(self.get_correct_pic((self.current_page - 1) * 6 + i)))
                self.comp_arr[i].setText(self.keys_list[(self.current_page - 1) * 6 + i])

    def left_page(self, MainWindow):
        if self.current_page > 1:
            self.current_page -= 1
            self.num_of_comps += 6
            self.page_num.setText(str(self.current_page))
            keys_list = list(self.comp_dict.keys())
            for index, i in enumerate(self.comp_arr):
                self.comp_arr[index].setVisible(True)
                self.images[index].setVisible(True)
                i.setText(keys_list[6 * (self.current_page - 1) + index])
                self.images[index].setPixmap(QtGui.QPixmap(self.get_correct_pic((self.current_page - 1) * 6 + index)))

    def scan(self, MainWindow):
        update_DB.main()
        comp_dict = update_DB.get_dict_data()
        num_of_comps = len(list(comp_dict.keys()))

        self.setupUi(MainWindow, num_of_comps, comp_dict)


def start_wins(comp_dict):
    num_of_comps = len(list(comp_dict.keys()))

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()

    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow, num_of_comps, comp_dict)

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    comp_dict = update_DB.get_dict_data()

    start_wins(comp_dict)