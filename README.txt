# Gears

The file gearCore.py contains the core functions to be imported and used in the other programs with a "from gearCore import *" statement.

The file gearGenerator.py will create a list of gear points and save them to a csv file named gearData.csv
The gear parameters used to generate the gear will be saved to a csv file named gearParameters.csv

The file gearModel.py is used to create a 3D model of 2 gears interacting and does so by loading data from gearData.csv and gearParameters.csv
The functions saveDataToCSV, readDataFromCSV, saveParametersToCSV and readParametersFromCSV will handle all of the reading and writing to csv files.

The file gearViewer.py can be used to view the gear in a matplotlib graph.