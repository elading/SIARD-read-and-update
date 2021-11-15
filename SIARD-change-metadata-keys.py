import xml.etree.ElementTree as ET
import pandas as pd
import tabulate

# Retrieve archive metadata file
xmlfil = r'\content\SIARDfile\header\metadata.xml'


root = ET.parse(xmlfil).getroot()

for child in root:
     print(child.tag)

tables = root.find("{*}schemas")[0].find("{*}tables")

data = []
for table in tables:
    data += [(table.find("{*}folder").text, table.find("{*}name").text)]

print(tabulate.tabulate(pd.DataFrame(data)))

# Finds primary keys:
data = []

for table in tables:
     if table.find("{*}primaryKey"):
            primkey = table.find("{*}primaryKey")
            data += [(table[1].text, table[0].text, primkey[0].text, primkey[1].text)]

print(tabulate.tabulate(pd.DataFrame(data)))

# Finds candidate keys:
data = []

for table in tables:
        if table.find("{*}candidateKeys"):    
            candkey = table.find("{*}candidateKeys")
            data += [(table[1].text, table[0].text, candkey[0][0].text, candkey[0][1].text)]

print(tabulate.tabulate(pd.DataFrame(data)))


# Finds foreignkeys
data = []
for table in tables:
    if table.find("{*}foreignKeys"):    
            foreignkey = table.find("{*}foreignKeys")
            data += [(table[1].text, table[0].text, foreignkey[0][0].text, foreignkey[0][1].text, foreignkey[0][2].text)]
            # ET.dump(table[0])
print(tabulate.tabulate(pd.DataFrame(data)))      


# Finds tables

data = []
for table in tables:
    data += [(table[1].text, table.find("{*}name").text)]
    
tabeller = pd.DataFrame(data)
print(tabulate.tabulate(tabeller))


def update_fk(tabellnummer, keynamepar, reftabpar, colpar, refcolpar):

    # Generating new element:
    
    keyselement = ET.Element('foreignKeys')
    keyelement = ET.SubElement(keyselement, 'foreignkey')
    ET.SubElement(keyelement, 'name')
    ET.SubElement(keyelement, 'referencedSchema')
    ET.SubElement(keyelement, 'referencedTable')
    referenceelement = ET.SubElement(keyelement, 'reference')
    ET.SubElement(referenceelement, 'column')
    ET.SubElement(referenceelement, 'referenced')

    ET.SubElement(keyelement, 'deleteAction')
    ET.SubElement(keyelement, 'updateAction')

    keyselement[0][1].text = 'DATABASENAME'
    keyselement[0][4].text = 'RESTRICT'
    keyselement[0][5].text = 'CASCADE'

    
    keyname = keynamepar
    reftab = reftabpar
    col = colpar
    refcol = refcolpar

    keyselement[0][0].text = keyname
    keyselement[0][2].text = reftab
    keyselement[0][3][0].text = col

    keyselement[0][3][1].text = refcol

    # PART 2 Generates a new table - newtable:
    
    if tables[tabellnummer].find("{*}foreignKeys"):

        newtable = ET.Element("table")
        
        newtable.extend(tables[tabellnummer][:5])
        newtable.append(keyselement)
        newtable.extend(tables[tabellnummer][5:])

    else:

        newtable = ET.Element("table")

        foreignkeys = ET.Element("foreignKeys")
        foreignkeys.extend(keyselement)

        newtable.extend(tables[tabellnummer][:5])
        newtable.append(foreignkeys)
        newtable.extend(tables[tabellnummer][5:])


    # Part 3 - replace the old table
    
    tables[tabellnummer] = newtable
    # ET.dump(newtable)

# example:
update_fk(134, "KRA_GRU_FK", "TU_VEDTAKSGRLAG", "GRUNNLAGSNR","GRUNNLAGSNR")
