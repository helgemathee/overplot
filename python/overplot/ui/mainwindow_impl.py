#
# Copyright (c) 2017-20187, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

from overplot import OVERPLOT_VERSION
from jogcontrolswidget_impl import JogControlsWidget
from logwidget_impl import LogWidget
from previewwidget_impl import PreviewWidget
from settingswidget_impl import SettingsWidget

class MainWindow(QtGui.QMainWindow):

  __settings = None

  def __init__(self):
    super(MainWindow, self).__init__()

    self.setWindowTitle("Overplot {0}".format(OVERPLOT_VERSION))

    previewWidget = PreviewWidget(self)
    self.setCentralWidget(previewWidget)

    self.__settings = QtCore.QSettings(self)

    settingsWidget = QtGui.QDockWidget('Settings', self)
    settingsWidget.setObjectName('settings')
    settingsWidget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
    settingsWidget.setWidget(SettingsWidget(settingsWidget, self.__settings))
    self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, settingsWidget)

    jogWidget = QtGui.QDockWidget('Jog Controls', self)
    jogWidget.setObjectName('jogcontrols')
    jogWidget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
    jogWidget.setWidget(JogControlsWidget(jogWidget))
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, jogWidget)

    logWidget = QtGui.QDockWidget('Log', self)
    logWidget.setObjectName('log')
    logWidget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
    logWidget.setWidget(LogWidget(logWidget))
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, logWidget)

    settingsWidget.widget().settingChangedMessage.connect(logWidget.widget().onLogEntryReceived)
    jogWidget.widget().jogRequestedMessage.connect(logWidget.widget().onLogEntryReceived)

    self.restoreGeometry(self.__settings.value("mainwindow.geometry"))
    self.restoreState(self.__settings.value("mainwindow.state"))

  def closeEvent(self, event):
    self.__settings.setValue("mainwindow.geometry", self.saveGeometry())
    self.__settings.setValue("mainwindow.state", self.saveState())
