#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from PySide import QtCore, QtGui

class JogControlsWidget(QtGui.QWidget):

  jogRequestedMessage = QtCore.Signal(str)
  moveRequested = QtCore.Signal(str, float)

  def __init__(self, parent):

    super(JogControlsWidget, self).__init__(parent)

    layout = QtGui.QGridLayout()
    self.setLayout(layout)

    self.setContentsMargins(5, 5, 5, 5)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(QtCore.Qt.AlignTop)

    s = 42
    bUp1mm = QtGui.QToolButton(self)
    bUp1mm.setText("1mm")
    bUp1mm.setMinimumSize(s, s)
    bLeft1mm = QtGui.QToolButton(self)
    bLeft1mm.setText("1mm")
    bLeft1mm.setMinimumSize(s, s)
    bRight1mm = QtGui.QToolButton(self)
    bRight1mm.setText("1mm")
    bRight1mm.setMinimumSize(s, s)
    bDown1mm = QtGui.QToolButton(self)
    bDown1mm.setText("1mm")
    bDown1mm.setMinimumSize(s, s)
    bUp10mm = QtGui.QToolButton(self)
    bUp10mm.setText("10mm")
    bUp10mm.setMinimumSize(s, s)
    bLeft10mm = QtGui.QToolButton(self)
    bLeft10mm.setText("10mm")
    bLeft10mm.setMinimumSize(s, s)
    bRight10mm = QtGui.QToolButton(self)
    bRight10mm.setText("10mm")
    bRight10mm.setMinimumSize(s, s)
    bDown10mm = QtGui.QToolButton(self)
    bDown10mm.setText("10mm")
    bDown10mm.setMinimumSize(s, s)
    bUp10cm = QtGui.QToolButton(self)
    bUp10cm.setText("10cm")
    bUp10cm.setMinimumSize(s, s)
    bLeft10cm = QtGui.QToolButton(self)
    bLeft10cm.setText("10cm")
    bLeft10cm.setMinimumSize(s, s)
    bRight10cm = QtGui.QToolButton(self)
    bRight10cm.setText("10cm")
    bRight10cm.setMinimumSize(s, s)
    bDown10cm = QtGui.QToolButton(self)
    bDown10cm.setText("10cm")
    bDown10cm.setMinimumSize(s, s)

    layout.addWidget(bUp10cm, 0, 3)
    layout.addWidget(bUp10mm, 1, 3)
    layout.addWidget(bUp1mm, 2, 3)
    layout.addWidget(bLeft10cm, 3, 0)
    layout.addWidget(bLeft10mm, 3, 1)
    layout.addWidget(bLeft1mm, 3, 2)
    layout.addWidget(bRight1mm, 3, 4)
    layout.addWidget(bRight10mm, 3, 5)
    layout.addWidget(bRight10cm, 3, 6)
    layout.addWidget(bDown1mm, 4, 3)
    layout.addWidget(bDown10mm, 5, 3)
    layout.addWidget(bDown10cm, 6, 3)

    bUp10cm.clicked.connect(lambda: self._onButtonPressed('Y', -100))
    bUp10mm.clicked.connect(lambda: self._onButtonPressed('Y', -10))
    bUp1mm.clicked.connect(lambda: self._onButtonPressed('Y', -1))
    bLeft10cm.clicked.connect(lambda: self._onButtonPressed('X', -100))
    bLeft10mm.clicked.connect(lambda: self._onButtonPressed('X', -10))
    bLeft1mm.clicked.connect(lambda: self._onButtonPressed('X', -1))
    bRight1mm.clicked.connect(lambda: self._onButtonPressed('X', 1))
    bRight10mm.clicked.connect(lambda: self._onButtonPressed('X', 10))
    bRight10cm.clicked.connect(lambda: self._onButtonPressed('X', 100))
    bDown1mm.clicked.connect(lambda: self._onButtonPressed('Y', 1))
    bDown10mm.clicked.connect(lambda: self._onButtonPressed('Y', 10))
    bDown10cm.clicked.connect(lambda: self._onButtonPressed('Y', 100))

  def _onButtonPressed(self, axis, mm):
    self.jogRequestedMessage.emit("Requested move on axis {0} for {1}".format(axis, mm))
    self.moveRequested.emit(axis, mm)
