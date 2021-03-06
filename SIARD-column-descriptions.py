# Necessary libraries

import xml.etree.ElementTree as ET
import pandas as pd
import tabulate

# Retrieve archive metadata file
xmlfil = r'\content\SIARDfile\header\metadata.xml'

root = ET.parse(metadata_fil).getroot()

tables = root.find("{*}schemas")[0].find("{*}tables")

# Prints table names:

for table in tables:
    print(table.find("{*}folder").text, table.find("{*}name").text)
    
# A specific table dump:

ET.dump(tables[15])


# Column descriptions:

for table in tables:
        columns = table.find("{*}columns")
        for column in columns:
            print(table[1].text, table[0].text, column[0].text, getattr(column.find('{*}description'), 'text', None))
            
# Adding an element:

ET.dump(tables[43].find("{*}columns"))
ET.dump(tables[43].find("{*}columns")[4])

new_element = ET.SubElement(tables[43].find("{*}columns")[4], 'description')
new_element.text = "beskrivelse"


ET.dump(tables[43].find("{*}columns"))
