#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

import os
import sys
import math
from PySide import QtCore, QtGui

class plotter(QtCore.QObject):

  __homePos = None
  __belts = None
  __servoAngle = None
  __simBelts = None
  __simServoAngle = None
  __settings = None

  __beltLength = None
  __stepperDistance = None
  __stepperDiameter = None

  __canvasWidth = None
  __canvasHeight = None
  __canvasOffset = None

  changed = QtCore.Signal()
  commandSent = QtCore.Signal(str)

  def __init__(self, parent, settings):
    super(plotter, self).__init__(parent)

    self.__settings = settings

    self.__homePos = (0, 0)
    self.__belts = (0, 0)
    self.__simBelts = (0, 0)
    self.__servoAngle = 0
    self.__simServoAngle = 0

    self.calibrate()

  @property
  def stepperDistance(self):
    return self.__stepperDistance

  def homeBelts(self, simulated=True):
    return self.__homePos

  def belts(self, simulated=True):
    if simulated:
      return self.__simBelts
    return self.__belts

  def remainingBelts(self, simulated=True):
    belts = self.belts(simulated=simulated)
    return (self.__beltLength - belts[0], self.__beltLength - belts[1])

  def servoAngle(self, simulated=True):
    if simulated:
      return self.__simServoAngle
    return self.__servoAngle

  def homePoint(self, w=None):
    (x, y) = self.__homePos

    x = x + self.__canvasOffset
    y = y + self.__canvasOffset

    if w:
      x = w * x / self.__canvasWidth
      y = w * y / self.__canvasWidth

    return QtCore.QPoint(x, y)

  def point(self, x=None, y=None, w=None):

    if x is None or y is None:
      (x, y) = self._posFromBelts(self.belts())

    x = x + self.__canvasOffset
    y = y + self.__canvasOffset

    if w:
      x = w * x / self.__canvasWidth
      y = w * y / self.__canvasWidth

    return QtCore.QPoint(x, y)

  @QtCore.Slot(str, float)
  def onSettingChanged(self, name, value):
    self.update()

  @QtCore.Slot(str, float)
  def onMoveRequested(self, axis, mm):
    if axis.lower() == 'x':
      self.move(mm, 0)
    else:
      self.move(0, mm)

  @QtCore.Slot(float)
  def onPenRequested(self, degrees):
    self.liftPen(degrees)

  def _posFromBelts(self, belts):
    (c, a) = belts
    b = float(self.__stepperDistance)
    angle = 0
    try:
      angle = math.acos((b * b + c * c - a * a) / (2.0 * b * c))
    except ValueError:
      pass
    except ZeroDivisionError:
      pass
    x = math.cos(angle) * c
    y = math.sin(angle) * c
    return (x, y)

  def _beltsFromPos(self, pos):
    x = float(pos[0])
    y = float(pos[1])
    x1 = self.__stepperDistance - x
    a = math.sqrt(x * x + y * y)
    c = math.sqrt(x1 * x1 + y * y)
    return (a, c)

  def _setBeltLengths(self, belts):
    self.__belts = belts
    self.__simBelts = belts
    self.changed.emit()

  def move(self, x, y, relative = True):
    if relative:
      p = self._posFromBelts(self.__belts)
      x = x + p[0]
      y = y + p[1]
    else:
      x = x + self.__homePos[0]
      y = y + self.__homePos[0]

    # todo: introduce a safezone

    if y < 0:
      return

    if x < 0 or x > self.__stepperDistance:
      return

    # if self.isPenDown():
    # todo: cut up the commands into very small sections

    (l, r) = self._beltsFromPos((x, y))

    if l > self.__beltLength:
      return
    if r > self.__beltLength:
      return

    self._setBeltLengths((l, r))

    command = 'G0'
    if self.isPenDown():
      command = 'G1'

    self.commandSent.emit('{0} X{1} Y{2}'.format(command, l, r))

  def liftPen(self, absAngle):
    if absAngle < 0 or absAngle > 90:
      return
    if self.__simServoAngle == absAngle:
      return

    self.__simServoAngle = absAngle

    if self.isPenDown():
      self.commandSent.emit('M5')
    else:
      self.commandSent.emit('M3 S{0}'.format(absAngle))

  def isPenDown(self):
    return self.__simServoAngle == 0

  def update(self):

    prevBeltLength = self.__beltLength
    prevStepperDistance = self.__stepperDistance

    self.__beltLength = float(self.__settings.value('settings.beltlength', 1000))
    self.__stepperDistance = float(self.__settings.value('settings.left2right', 2000))
    self.__stepperDiameter = float(self.__settings.value('settings.stepperDiameter', 12))

    if prevBeltLength != self.__beltLength or prevStepperDistance != self.__stepperDistance:
      self._computeHomePose()

    self.__canvasOffset = 250
    self.__canvasWidth = int(self.__stepperDistance) + 2 * self.__canvasOffset
    self.__canvasHeight = int(self.__beltLength * 0.75) + self.__canvasOffset

    self.changed.emit()

  def _computeHomePose(self):
    (homeX, homeY) = self._posFromBelts((self.__beltLength, self.__beltLength))
    homeY = homeY * 0.5
    self.__homePos = (homeX, homeY)

  def calibrate(self):
    self.update()

    left2gondola = float(self.__settings.value('settings.left2gondola', 150))
    right2gondola = float(self.__settings.value('settings.right2gondola', 150))

    self.__belts = (left2gondola, right2gondola)
    self.__simBelts = (left2gondola, right2gondola)

    self._computeHomePose()

    self.changed.emit()
