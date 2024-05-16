from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QTableWidget
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import Qt,QThread,QVariant
from PyQt5.QtGui import QBrush,QColor
import pandas as pd
from datetime import date
import time
import webbrowser
from main_window_ui import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(894, 603)
        self.inter=False
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
         excelFilePath=r"Price_Pulse\excel1.xlsx"
         worksheetName='Sheet1'

         self.data = self._data = pd.read_excel(excelFilePath,worksheetName).drop(['Gem_Catalogue_Id','Quantity','Inventory_Status'],axis=1)
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
        self.data = self.data.sort_values(dict[index], ascending=False)
        self.model2=TableModel(self.data)
        self.tableView.setModel(self.model2)

    def reset(self):
        self.tableView.setModel(self.model)


class TableModel(QtGui.QStandardItemModel):

    def __init__(self, data, parent=None):
           QtGui.QStandardItemModel.__init__(self, parent)
           self.currentRow=0
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
                return str(self._data.iloc[index.row(), index.column()])
        elif role == Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
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



app=QApplication([])
window=Window()
app.setStyle("Fusion")
window.show()
app.exec()
