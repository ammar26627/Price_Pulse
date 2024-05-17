from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QLabel,QVBoxLayout
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import Qt,QThread,QVariant
from PyQt5.QtGui import QBrush,QColor
import pandas as pd
from datetime import date
import time
import webbrowser
from main_window_ui import Ui_MainWindow
import os.path
import sys

class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        fullpath = os.path.abspath('..\Price_Pulse\icon.png')
        self.setWindowIcon(QtGui.QIcon(fullpath))
        self.setWindowTitle('PricePulse')
        self.setFixedSize(894, 603)
        self.inter=False
        self.tableView.setShowGrid(False)
        self.StartButton.clicked.connect(self.startButtonClicked)
        self.stopButton.clicked.connect(self.stop)
        self.dateUpdate.setText(f'Last Updated On: {date.today()}')
        self.searchBox.setPlaceholderText("Search...")
        self.searchBox.textChanged.connect(self.myfilter)
        self.tableView.doubleClicked.connect(self.openLink)
        self.comboBox_2.currentIndexChanged.connect(self.sort)
        self.resetButton.clicked.connect(self.reset)

    def startButtonClicked(self):
        self.worker=Worker()
        self.worker.start()
        self.worker.updateProgress.connect(self.updateProgress)
        self.worker.finished.connect(self.getResults)
    def updateProgress(self,value):
        self.progressBar.setValue(value)
    def stopStatus(self):
        return self.inter    
    
    def stop(self):
        self.inter=True

    def getResults(self):
         fullpath = os.path.abspath('..\Price_Pulse\excel1.xlsx')
         worksheetName='Sheet1'

         self.data = self._data = pd.read_excel(fullpath,worksheetName).drop(['Gem_Catalogue_Id','Quantity','Inventory_Status','Product_Status'],axis=1)
         self.model = TableModel(self.data)
         self.tableView.setModel(self.model)

    def myfilter(self,regex: str, case=False):
        df=self.data
        match = df.select_dtypes(include=[object, "string"])
        match=df[match.apply(lambda column: column.str.contains(regex, regex=True, case=case, na=False)).any(axis=1)]
        self.model1=TableModel(match)
        self.tableView.setModel(None)
        self.tableView.setModel(self.model1)

    def openLink(self):
        for index in self.tableView.selectionModel().selectedIndexes():
            value = str(self.data.iloc[index.row()][index.column()])
            if value.startswith("http://") or value.startswith("https://"):
                webbrowser.open(value)

    def sort(self,index):
        dict={1:'Our_Price',2:'Other_Seller_Price'}
        try:
             self.data = self.data.sort_values(dict[index], ascending=False)
        except AttributeError:
            self.show_dialog("Please Load Data First")
        else:
            self.model2=TableModel(self.data)
            self.tableView.setModel(self.model2)

    def reset(self):
        self.tableView.setModel(self.model)

    def show_dialog(self,text):
        dialog = QDialog(self)
        dialog.setWindowTitle("Error")
        label = QLabel(text)
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(label)
        dialog.setLayout(dialog_layout)
        dialog.exec_()

class TableModel(QtGui.QStandardItemModel):

    def __init__(self, data, parent=None):
           QtGui.QStandardItemModel.__init__(self, parent)
           self._data = data
           for row in data.values.tolist():

               data_row = [ QtGui.QStandardItem("{}".format(x)) for x in row ]
               self.appendRow(data_row)
           return

    def data(self, index, role):
        if role == Qt.ForegroundRole:
            value = str(self._data.iloc[index.row(),index.column()])
            if value.startswith("https://") or value.startswith("http://"):
                return QtGui.QColor("blue")
        elif role == Qt.DisplayRole:
                value = str(self._data.iloc[index.row(),index.column()])
                if value.startswith("https://") or value.startswith("http://"):
                    return ('Click To Open Link')
                return value
        if role == Qt.BackgroundRole and index.column()==7:
                try:
                    if (int(self._data.iloc[index.row(),7]) >= int(self._data.iloc[index.row(),9])):
                        return QVariant(QColor(QtCore.Qt.green))
                    else:
                        return QVariant(QColor(QtCore.Qt.red))
                except ValueError:
                        return QVariant(QColor(QtCore.Qt.yellow))



    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def headerData(self, x, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[x]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[x]
        return None
    
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | ~Qt.ItemIsEditable
    

class Worker(QThread):
    updateProgress=QtCore.pyqtSignal(int)
    def run(self):
        self.inter=False
        for i in range(1,101): 
            time.sleep(0.05) 
            self.updateProgress.emit(i)
            self.inter=window.stopStatus()
            if self.inter:
                window.inter=False
                break



app=QApplication(sys.argv)
window=Window()
app.setStyleSheet('''QMainWindow {
	background-color:#1e1d23;
}
QDialog {
	background-color:#1e1d23;
}
QColorDialog {
	background-color:#1e1d23;
}
QTextEdit {
	background-color:#1e1d23;
	color: #a9b7c6;
}
QPlainTextEdit {
	selection-background-color:#007b50;
	background-color:#1e1d23;
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	color: #a9b7c6;
}
QPushButton{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QPushButton::default{
	border-style: inset;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-width: 1px;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QToolButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 2px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QPushButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 1px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 2px;
	background-color: #1e1d23;
}
QPushButton:pressed{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 2px;
	border-style: solid;
	color: #37efba;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QPushButton:disabled{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #808086;
	border-bottom-width: 2px;
	border-style: solid;
	color: #808086;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QLineEdit {
	border-width: 1px; border-radius: 4px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	padding: 0 8px;
	color: #a9b7c6;
	background:#1e1d23;
	selection-background-color:#007b50;
	selection-color: #FFFFFF;
}
QLabel {
	color: #a9b7c6;
}
QProgressBar {
	text-align: center;
	color: rgb(240, 240, 240);
	border-width: 1px; 
	border-radius: 10px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	background-color:#1e1d23;
}
QProgressBar::chunk {
	background-color: #04b97f;
	border-radius: 5px;
}
QMenuBar {
	background-color: #1e1d23;
}
QMenuBar::item {
	color: #a9b7c6;
  	spacing: 3px;
  	padding: 1px 4px;
  	background: #1e1d23;
}

QMenuBar::item:selected {
  	background:#1e1d23;
	color: #FFFFFF;
}
QMenu::item:selected {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: #04b97f;
	border-bottom-color: transparent;
	border-left-width: 2px;
	color: #FFFFFF;
	padding-left:15px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color: #1e1d23;
}
QMenu::item {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding-left:17px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color: #1e1d23;
}
QMenu{
	background-color:#1e1d23;
}
QTabWidget {
	color:rgb(0,0,0);
	background-color:#1e1d23;
}
QTabWidget::pane {
		border-color: rgb(77,77,77);
		background-color:#1e1d23;
		border-style: solid;
		border-width: 1px;
    	border-radius: 6px;
}
QTabBar::tab {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #808086;
	padding: 3px;
	margin-left:3px;
	background-color: #1e1d23;
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-bottom-width: 2px;
	border-style: solid;
	color: #FFFFFF;
	padding-left: 3px;
	padding-bottom: 2px;
	margin-left:3px;
	background-color: #1e1d23;
}

QComboBox {
	color: #a9b7c6;	
	background: #1e1d23;
}
QComboBox:editable {
	background: #1e1d23;
	color: #a9b7c6;
	selection-background-color: #1e1d23;
}
QComboBox QAbstractItemView {
	color: #a9b7c6;	
	background: #1e1d23;
	selection-color: #FFFFFF;
	selection-background-color: #1e1d23;
}
QComboBox: !editable:on, QComboBox::drop-down:editable:on {
	color: #a9b7c6;	
	background: #1e1d23;
}

''')
app.setStyle("Fusion")
window.show()
app.exec()
