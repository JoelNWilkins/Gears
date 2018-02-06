# Gears

The file gearCore.py contains the core functions to be imported and used in the other programs with a "from gearCore import *" statement.

The file gearGenerator.py will create a list of gear points and save them to an xls file named containing a page with the points and a page with the parameters.

The file gearModel.py is used to create a 3D model of 2 gears interacting and does so by loading data from an xls file

The file gearViewer.py can be used to view the gear in a matplotlib graph. This program contains classes for the graph frame and the menubar and is imported to gearGenerator.py which adds to the gear viewer interface.