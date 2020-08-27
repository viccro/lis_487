#!/usr/local/bin/python3

import sys
import csv
import xmlschema
import xml.etree.ElementTree as ET

xsd = "data/budgets.xsd"
myschema = xmlschema.XMLSchema(xsd)
xml_out = "output.xml"

def main(csv_path):
    root = ET.Element('budget')


    with open(csv_path, newline='') as input_file:
        filereader = csv.DictReader(input_file, fieldnames=['name','email','category','price','date'])

        for row in filereader:
            bi = ET.SubElement(root, 'budget_item')

            name = ET.SubElement(bi, "name")
            first = ET.SubElement(name, "firstname")
            first.text = row['name'].split(' ', 1)[0]

            last = ET.SubElement(name, "lastname")
            last.text = row['name'].split(' ', 1)[1]

            em = ET.SubElement(bi, 'email')
            em.text = row['email']

            amt = ET.SubElement(bi, "amount")
            amt.text = row['price'].strip('$')

            cat = ET.SubElement(bi, 'category')
            cat.text = row['category']

            date = ET.SubElement(bi, "date")
            date.text = row['date']

    xml = ET.tostring(root, encoding='UTF-8').decode()

    with open(xml_out, 'w') as writer:
        writer.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        writer.write(xml)

    print(schema_is_valid(xml_out))

def schema_is_valid(xml_file):
    return myschema.is_valid(xml_file)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Be sure you include the relative path to the csv data input")