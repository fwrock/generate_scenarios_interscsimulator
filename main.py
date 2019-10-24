from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
import shutil
import random

#parse an xml file by name
map = minidom.parse("assets/map.xml")

nodes = map.getElementsByTagName('node')
links = map.getElementsByTagName('link')


cwd = os.getcwd()
outputPath = os.path.join(cwd, "./output")
scenarioName = "sp_simplificado"
simulationTime = 86400
numberOfTrips = 50000

scenarioPath = os.path.join(outputPath, "./"+scenarioName)
if not os.path.exists(scenarioPath):
    os.mkdir(scenarioPath)

#Create config file
print('Creating configuration file...')
scsimulatorConfig = ET.Element('scsimulator_config')
config = ET.SubElement(scsimulatorConfig, 'config')
config.set('traffic_signals_file', '../'+scenarioName+'/signals.xml')
config.set('trip_file', '../'+scenarioName+'/trips.xml')
config.set('map_file', '../'+scenarioName+'/map.xml')
config.set('output_file', '../'+scenarioName+'/events.xml')
config.set('metro_file', '../'+scenarioName+'/metro.xml')
config.set('bus_file', '../'+scenarioName+'/buses.xml')
config.set('digital_rails_file', '../'+scenarioName+'/empty-digital-rails.xml')
config.set('simulation_time', str(simulationTime))

configFileData = ET.tostring(scsimulatorConfig)
configFile = open(scenarioPath+"/config.xml", "w")
configFile.write(str(configFileData).replace('b', '').replace('\'', ''))

#copy default files to new scenario folder
print('Creating copy of default file to new scenario folder...')
shutil.copy('assets/map.xml', scenarioPath+'')
shutil.copy('assets/empty-digital-rails.xml', scenarioPath+'')
shutil.copy('assets/metro.xml', scenarioPath+'')
shutil.copy('assets/buses.xml', scenarioPath+'')
shutil.copy('assets/park.csv', scenarioPath+'')
shutil.copy('assets/signals.xml', scenarioPath+'')
shutil.copy('assets/empty-signals.xml', scenarioPath+'')


print('Creating file trips...')

scsimulatorMatrix = ET.Element('scsimulator_matrix')
print('Creating trips...')
for i in range(numberOfTrips):
    trip = ET.SubElement(scsimulatorMatrix, 'trip')
    trip.set('origin', str(nodes[random.randint(0, len(nodes)-1)].attributes['id'].value))
    trip.set('destination', str(nodes[random.randint(0, len(nodes)-1)].attributes['id'].value))
    trip.set('link_origin', str(links[random.randint(0, len(links)-1)].attributes['id'].value))
    trip.set('count', '1')
    trip.set('start', str(random.randint(1, simulationTime)))
    trip.set('digital_rails_capable', 'false')

print(str(numberOfTrips)+' were created!')

tripsFileData = ET.tostring(scsimulatorMatrix)
tripFile = open(scenarioPath+'/trips.xml', 'w')
tripFile.write(str(tripsFileData).replace('b', '').replace('\'', ''))

print('Trips were salved!')
print('Finished!!')