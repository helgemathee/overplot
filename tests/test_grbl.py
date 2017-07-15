#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from overplot.models.grbl_impl import grbl


g = grbl('COM3')

g.connect()
g.disconnect()
