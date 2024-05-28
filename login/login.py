from login_window_ui import Ui_login_window
from trial_window_ui import Ui_trial_window
from PyQt5.QtWidgets import QWidget,QLineEdit,QApplication
from PyQt5.QtGui import QIcon
import sys,os
import re




class Window(QWidget, Ui_login_window):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        fullpath = os.path.abspath('icon.png')
        self.sign_up.setStyleSheet('''border-color: #1e1d23;
         color: #AAFF00                          ''')
        self.setWindowIcon(QIcon(fullpath))
        self.email_edit.textChanged.connect(self.email)
        self.number_edit.textChanged.connect(self.number)
        self.sign_up.clicked.connect(self.trial)
    
    def email(self,emailid):
            regex=r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
            if re.match(regex,emailid,re.IGNORECASE):
                 self.emailid=emailid
    def number(self,number):
         if re.match(r'[0-9]{10}',number):
              print(number)
    def trial(self):
         self.trial_window=TrialWindow()
         self.trial_window.show()
         

class TrialWindow(QWidget,Ui_trial_window):
     def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        fullpath = os.path.abspath('icon.png')
        self.setWindowIcon(QIcon(fullpath))
        self.email_edit.textChanged.connect(self.email)
        self.number_edit.textChanged.connect(self.number)
     def email(self,emailid):
        regex=r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
        if re.match(regex,emailid,re.IGNORECASE):
                 self.emailid=emailid
     def number(self,number):
        if re.match(r'[0-9]{10}',number):
              print(number)
     def product(self):
          ...
        
     

app=QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
app.setStyleSheet('''

QWidget {
	background-color:#1e1d23;
}
QTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
	background-color: #222b2e;
	color: #d3dae3;
}
QPlainTextEdit {
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
	background-color: #222b2e;
	color: #d3dae3;
}

QPushButton{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #d3dae3;
	padding: 2px;
	background-color: #1e1d23;
}
QPushButton::default{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #FFFFFF;
	padding: 2px;
	background-color: #1e1d23;;
}
QPushButton:hover{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #d3dae3;
	padding: 2px;
	background-color: #1c1f1f;
}
QPushButton:pressed{
	border-style: solid;
	border-color: #050a0e;
	border-width: 1px;
	border-radius: 5px;
	color: #d3dae3;
	padding: 2px;
	background-color: #2c2f2f;
}
QPushButton:disabled{
	border-style: solid;
	border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-right-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(217, 217, 217), stop:1 rgb(227, 227, 227));
	border-left-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(227, 227, 227), stop:1 rgb(217, 217, 217));
	border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(215, 215, 215), stop:1 rgb(222, 222, 222));
	border-width: 1px;
	border-radius: 5px;
	color: #808086;
	padding: 2px;
	background-color: rgb(142,142,142);
}
QLineEdit {
	border-width: 1px;
	border-style: solid;
	border-color: #4fa08b;
	background-color: #222b2e;
	color: #d3dae3;
}
QLabel {
	color: #d3dae3;
}


QCheckBox {
	color: #d3dae3;
	padding: 2px;
}
QCheckBox:disabled {
	color: #808086;
	padding: 2px;
}

QCheckBox:hover {
	border-radius:4px;
	border-style:solid;
	padding-left: 1px;
	padding-right: 1px;
	padding-bottom: 1px;
	padding-top: 1px;
	border-width:1px;
	border-color: transparent;
}
QCheckBox::indicator:checked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #4fa08b;
	color: #000000;
	background-color: qradialgradient(cx:0.4, cy:0.4, radius: 1.5,fx:0, fy:0, stop:0 #1e282c, stop:0.3 #1e282c, stop:0.4 #4fa08b, stop:0.5 #1e282c, stop:1 #1e282c);
}
QCheckBox::indicator:unchecked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #4fa08b;
	color: #000000;
}
QRadioButton {
	color: #d3dae3;
	padding: 1px;
}
QRadioButton::indicator:checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #4fa08b;
	color: #a9b7c6;
	background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #4fa08b, stop:1 #1e282c);
}
QRadioButton::indicator:!checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #4fa08b;
	color: #a9b7c6;
	background-color: transparent;
}
QStatusBar {
	color:#027f7f;
}
''')
app.setStyle("Fusion")
window=Window()
window.show()
app.exec()