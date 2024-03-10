from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import process_check


class Ui_Form(object):
    def setupUi(self, form, ip):
        self.form = form
        self.ip = ip
        self.form.setObjectName("Form")
        self.form.resize(756, 606)
        self.label = QtWidgets.QLabel(self.form)
        self.label.setGeometry(QtCore.QRect(180, 30, 331, 101))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.form)
        self.pushButton.setGeometry(QtCore.QRect(100, 130, 541, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.form)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 230, 541, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.form)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 330, 541, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_2")
        self.pushButton_3.clicked.connect(self.show_processes)
        self.retranslateUi(self.form)
        QtCore.QMetaObject.connectSlotsByName(self.form)

        self.widgets = QtWidgets.QStackedWidget()
        self.widgets.addWidget(self.form)
        self.widgets.setFixedWidth(756)
        self.widgets.setFixedHeight(606)
        self.widgets.show()

    def show_processes(self):
        print(self.widgets.__len__())
        self.form.close()
        self.proc_win = ProcessWin()
        self.proc_win.start_ui(self.widgets)
        self.widgets.addWidget(self.proc_win)
        self.widgets.setCurrentIndex(self.widgets.currentIndex() + 1)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", f"Options for {self.ip}"))
        self.pushButton.setText(_translate("Form", "Scan windows files"))
        self.pushButton_2.setText(_translate("Form", "Check camera and microphone"))
        self.pushButton_3.setText(_translate("Form", "Check processes"))


class ProcessWin(QtWidgets.QWidget):
    def start_ui(self, widget):
        self.widget = widget
        self.proc_dict = process_check.get_proc_dict()
        font = QtGui.QFont()
        font.setPointSize(16)

        self.formlayout = QtWidgets.QFormLayout()
        self.group_box = QtWidgets.QGroupBox("Elevated processes:")
        self.group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.group_box.setFont(font)

        self.label_list = []
        self.button_list = []
        for i in range(len(self.proc_dict)):
            self.draw_box(font, i)

        self.group_box.setLayout(self.formlayout)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.group_box)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(325, 520, 100, 50))
        self.back_button.setText("Go back")
        self.back_button.clicked.connect(self.go_to_main_screen)

    def draw_box(self, font, i):
        print(list(self.proc_dict.values())[i])
        self.label_list.append(QtWidgets.QLabel(f"PID: {str(list(self.proc_dict.values())[i])}"))
        self.button_list.append(QtWidgets.QPushButton(f"Process name: {list(self.proc_dict.keys())[i]}"))
        self.label_list[i].setFont(font)
        self.button_list[i].setFont(font)
        self.button_list[i].clicked.connect(lambda: self.clicked_proc(i))
        self.formlayout.addRow(self.label_list[i], self.button_list[i])

    def clicked_proc(self, index):
        self.proc_opt = ProcessOptions()
        self.proc_opt.start_ui(self.widget, list(self.proc_dict.keys())[index], list(self.proc_dict.values())[index])
        self.widget.addWidget(self.proc_opt)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_to_main_screen(self):
        self.close()
        self.widget.removeWidget(self)
        self.widget.setCurrentIndex(0)


class ProcessOptions(QtWidgets.QWidget):
    def start_ui(self, widget, pname, pid):
        self.widget = widget
        self.pname = pname
        self.pid = pid

        self.proc_lable = QtWidgets.QLabel(self)
        self.proc_lable.setGeometry(QtCore.QRect(80, 40, 600, 50))
        self.proc_lable.setText(f"Process: {pname}")
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.proc_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.proc_lable.setFont(font)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(325, 520, 100, 50))
        self.back_button.setText("Go back")
        self.back_button.clicked.connect(self.go_back)

        self.reduce_privs_button = QtWidgets.QPushButton(self)
        self.reduce_privs_button.setGeometry(120, 330, 200, 50)
        self.reduce_privs_button.setText("Reduce process privileges")
        self.reduce_privs_button.clicked.connect(self.reduce_privs)

        self.close_proc_button = QtWidgets.QPushButton(self)
        self.close_proc_button.setGeometry(425, 330, 200, 50)
        self.close_proc_button.setText("Close process")
        self.close_proc_button.clicked.connect(self.close_proc)

    def go_back(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)
        self.widget.removeWidget(self)

    def reduce_privs(self):
        process_check.disable_privs(self.pid)

    def close_proc(self):
        process_check.close_proc(self.pid)
