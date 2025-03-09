from os import read
import xml.etree.ElementTree as ET
from xml.dom import minidom

root = ET.Element('trainlogs')

def convertLogsToXML(filepath, name):
    for line in open(filepath, 'r'):
        parts = line.strip().split(',')
        
        logid = ET.SubElement(root, 'log')
        date = ET.SubElement(logid, 'Date')
        train = ET.SubElement(logid, 'Train')
        trainset = ET.SubElement(train, 'Set')
        traintype = ET.SubElement(train, 'Type')
        trip = ET.SubElement(logid, 'Trip')
        
        line = ET.SubElement(trip, 'Line')
        start = ET.SubElement(trip, 'Start')
        end = ET.SubElement(trip, 'End')
        
        notes = ET.SubElement(logid, 'Notes')
        

        logid.set('id', parts[0])
        trainset.text = parts[1]
        traintype.text = parts[2]
        date.text = parts[3]
        line.text = parts[4]
        start.text = parts[5]
        end.text = parts[6]
        notes.text = parts[7]


    xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml()
    with open(f'temp/{name}.xml', 'w') as file:
        file.write(xmlStr)
    return f'temp/{name}.xml'
    
def readXML(user, sid):
    tree = ET.parse(f'temp/{user}.xml')
    root = tree.getroot()
    for log in root.findall('log'):
        logid = log.get('id')
        if logid == sid:
            date = log.find('Date').text
            trainset = log.find('Train/Set').text
            traintype = log.find('Train/Type').text
            line = log.find('Trip/Line').text
            start = log.find('Trip/Start').text
            end = log.find('Trip/End').text
            notes = log.find('Notes').text
            print(f'Log ID: {logid}\nDate: {date}\nTrain Set: {trainset}\nTrain Type: {traintype}\nLine: {line}\nStart: {start}\nEnd: {end}\nNotes: {notes}\n\n')

# convertLogsToXML('xm9g')
# readXML('xm9g', "#100")