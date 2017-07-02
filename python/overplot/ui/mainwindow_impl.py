#
# Copyright (c) 2017-20187, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

from overplot import OVERPLOT_VERSION
from settingswidget_impl import SettingsWidget
from jogcontrolswidget_impl import JogControlsWidget
from logwidget_impl import LogWidget

class MainWindow(QtGui.QMainWindow):

  def __init__(self):
    super(MainWindow, self).__init__()

    self.setWindowTitle("Overplot {0}".format(OVERPLOT_VERSION))

    centralWidget = QtGui.QWidget(self)
    self.setCentralWidget(centralWidget)

    settings = QtCore.QSettings(self)

    settingsWidget = QtGui.QDockWidget('Settings', self)
    settingsWidget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
    settingsWidget.setWidget(SettingsWidget(settingsWidget, settings))
    self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, settingsWidget)

    jogWidget = QtGui.QDockWidget('Jog Controls', self)
    jogWidget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
    jogWidget.setWidget(JogControlsWidget(jogWidget))
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, jogWidget)

    logWidget = QtGui.QDockWidget('Log', self)
    logWidget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
    logWidget.setWidget(LogWidget(logWidget))
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, logWidget)

    settingsWidget.widget().settingChangedMessage.connect(logWidget.widget().onLogEntryReceived)
    jogWidget.widget().jogRequestedMessage.connect(logWidget.widget().onLogEntryReceived)
