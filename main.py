import sys, inspect
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from gui.PandasModel import PandasModel

import pandas as pd

from gui.startupdialog import *



class StartUpDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Input_File()
        self.ui.setupUi(self)
        self.show()



class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("gui/mainwindow.ui",self)

        self.setWindowTitle("Trace Analyzer")
        fileAction = QAction("&New File",self)
        fileAction.setShortcut("Ctrl+N")
        fileAction.setStatusTip("&Input a New File")
        fileAction.triggered.connect(self.new_file)

        fileMenu = self.menubar.addMenu("&File")
        fileMenu.addAction(fileAction)

        helpAction = QAction("&Help",self)
        helpAction.setShortcut("F1")
        helpAction.setStatusTip("&Help")
        helpAction.triggered.connect(self.help_act)

        aboutAction = QAction("&About",self)
        aboutAction.setStatusTip("&About")
        aboutAction.triggered.connect(self.about_act)

        helpMenu = self.menubar.addMenu("&Help")
        helpMenu.addAction(helpAction)
        helpMenu.addAction(aboutAction)



        self.CurParameter = "Lambda(\u03BB)"
        self.parameter_combo.currentIndexChanged.connect(self.parameterChanged)
        self.node_combo.currentIndexChanged.connect(self.nodeChanged)

        self.update_files()
        self.update_comboBox()
        self.update_csv()

        self.addToolBar(NavigationToolbar(self.Mplwidget.canvas, self))

    def update_files(self):
        self.partialpath = (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))+ "/csvfiles/parameters.csv"
        self.completelpath = (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))+ "/csvfiles/complete.csv"
        self.partialcsv_helper = pd.read_csv(self.partialpath)
        self.completecsv_helper = pd.read_csv(self.completelpath)

    def update_comboBox(self):
        self.node_combo.clear()
        self.node_combo.addItems(list(map(str,(self.partialcsv_helper['Node'].tolist()))))
        self.node_combo.addItem("All")

        self.listparameters = (list(self.partialcsv_helper))
        self.listparameters.pop(0)
        self.parameter_combo.clear()
        self.parameter_combo.addItems(self.listparameters)

        self.CurParameter = self.parameter_combo.currentText()
        self.CurNode = self.node_combo.currentText()

    def update_csv(self):
        model = PandasModel(self.partialcsv_helper)
        self.csv_parcial.setSortingEnabled(True)
        self.csv_parcial.setModel(model)

        model = PandasModel(self.completecsv_helper)
        self.csv_complete.setSortingEnabled(True)
        self.csv_complete.setModel(model)

    def parameterChanged(self):
        self.CurParameter = self.parameter_combo.currentText()
        self.update_graph()

    def nodeChanged(self):
        self.CurNode = self.node_combo.currentText()
        self.update_graph()

    def update_graph(self):

        if not self.CurNode == "All":
            self.partnodegraph = self.completecsv_helper[self.completecsv_helper.Node.eq(int(self.CurNode))]
            self.parameter = self.partnodegraph[self.CurParameter]
            self.time = self.partnodegraph['Time']
            self.Mplwidget.canvas.axes.clear()
            self.Mplwidget.canvas.axes.plot(self.time, self.parameter)
            self.Mplwidget.canvas.axes.legend((self.CurParameter),loc='upper right')
            self.Mplwidget.canvas.axes.set_title(self.CurParameter + ' signal (' + self.CurNode + ')')
            self.Mplwidget.canvas.draw()
        else:
            self.time = self.completecsv_helper['Time']
            self.parameter = self.completecsv_helper[self.CurParameter]
            self.Mplwidget.canvas.axes.clear()
            self.Mplwidget.canvas.axes.plot(self.time, self.parameter)
            self.Mplwidget.canvas.axes.legend((self.CurParameter),loc='upper right')
            self.Mplwidget.canvas.axes.set_title(self.CurParameter + ' signal (All nodes)')
            self.Mplwidget.canvas.draw()

    def update_comboBox_node(self):
        self.node_combo.clear()
        self.node_combo.addItems(list(map(str,(self.partialcsv_helper['Node'].tolist()))))
        self.node_combo.addItem("All")
        self.CurNode = self.node_combo.currentText()

    def new_file(self):
        options = QFileDialog.Options()
        fn = QFileDialog.getOpenFileName(None,"Open File", "/home/", ("Tracer (*.tr)"))
        analyzer(fn[0])

        self.update_files()
        self.update_csv()
        self.update_graph()

    def help_act(self):
        quit_msg = 'º Graph: You can see the variation of parameters and nodes of your choice. \n\nº Table: See the full only the final results or variation respectively. \n\nº To iniciate a new file press "Ctrl + F" or go to file and press "New File" to put another .tr file'
        qb = QtWidgets.QMessageBox
        reply = qb.question(self, 'Message', quit_msg, qb.Ok)

        if reply == qb.Ok:
            return True

    def about_act(self):
        quit_msg = 'Um software capaz de interpretar dados do trace gerado pelo simulador NS-3. O código compõe o projeto de trabalho de conclusão e Iniciação cientifica na Universidade Federal de Santa Catarina - Centro Tecnológico de Joinville.'
        qb = QtWidgets.QMessageBox
        reply = qb.question(self, 'Message', quit_msg, qb.Ok)

        if reply == qb.Ok:
            return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if StartUpDialog().exec() == QDialog.Accepted:
        window = MatplotlibWidget()
        window.show()
        sys.exit(app.exec_())
