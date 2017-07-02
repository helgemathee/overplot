#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

class SettingsWidget(QtGui.QWidget):

  __fields = None
  __settings = None
  settingChanged = QtCore.Signal(str, float)
  settingChangedMessage = QtCore.Signal(str)

  def __init__(self, parent, settings):

    super(SettingsWidget, self).__init__(parent)

    self.__settings = settings

    layout = QtGui.QGridLayout()
    self.setLayout(layout)

    self.setContentsMargins(5, 5, 5, 5)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(QtCore.Qt.AlignTop)

    self.__toggleLocked = QtGui.QPushButton('Unlock', self)
    layout.addWidget(self.__toggleLocked, 0, 1)
    self.connect(self.__toggleLocked, QtCore.SIGNAL('clicked()'), self.onToggleLocked)

    self.__fields = {}

    def addField(self, key, title):
      row = self.layout().rowCount()
      self.__fields[key] = QtGui.QLineEdit(self)
      self.__fields[key].setObjectName(key)
      self.__fields[key].setValidator(QtGui.QDoubleValidator())
      self.__fields[key].setEnabled(False)
      self.__fields[key].setText(str(self.getValue(key, 0.0)))
      self.connect(self.__fields[key], QtCore.SIGNAL('editingFinished()'), self.onSettingChanged)
      self.layout().addWidget(QtGui.QLabel(title, self), row, 0)
      self.layout().addWidget(self.__fields[key], row, 1)

    addField(self, 'height', 'Stepper Height (mm)')
    addField(self, 'left2right', 'Stepper to Stepper (mm)')
    addField(self, 'left2gondola', 'Left Stepper to Gondola (mm)')
    addField(self, 'right2gondola', 'Right Stepper to Gondola (mm)')
    addField(self, 'stepperDiameter', 'Stepper Diameter (mm)')

  def onToggleLocked(self):
    for key in self.__fields:
      enabled = not self.__fields[key].isEnabled()
      self.__fields[key].setEnabled(enabled)

    if enabled:
      self.__toggleLocked.setText('Lock')
    else:
      self.__toggleLocked.setText('Unlock')

  def onSettingChanged(self):
    text = self.sender().text()
    if not text:
      return
    key = self.sender().objectName()
    prev = self.getValue(key, -100000)
    if float(prev) == float(text):
      return
    self.setValue(key, float(text))
    self.settingChanged.emit(key, float(text))
    self.settingChangedMessage.emit("Setting: {0} = {1}".format(key, text))

  def getValue(self, name, default):
    return self.__settings.value('settings.{0}'.format(name), default)

  def setValue(self, name, value):
    self.__settings.setValue('settings.{0}'.format(name), value)
