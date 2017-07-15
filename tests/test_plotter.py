#
# Copyright (c) 2017-2018, Helge Mathee. All rights reserved.
#

from overplot.plotter_impl import plotter

def test_plotter():

  p = plotter()
  assert ( p.stepperCount == 0 )
