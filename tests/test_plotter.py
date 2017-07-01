from overplot.plotter_impl import plotter

def test_plotter():

  p = plotter()
  assert ( p.stepperCount == 0 )
