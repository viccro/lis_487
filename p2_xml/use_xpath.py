#!/usr/local/bin/python3

import sys
import csv
import xmlschema
import xml.etree.ElementTree as ET

xsd = "data/budgets.xsd"
myschema = xmlschema.XMLSchema(xsd)

def main(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    get_low_spenders(root)
    get_computer_buyers(root)
    get_03_17_spenders(root)

def get_low_spenders(root):
    print("Low spenders:\n")
    for item in root.findall("./budget_item"):
        if (float(item.find("amount").text) < 5):
            print(item.find("email").text,"-", item.find("category").text)

def get_computer_buyers(root):
    print("Computer buying dates: ")
    datelist = []
    for item in root.findall("./budget_item"):
        if (item.find("category").text) == "Computers":
            datelist.append(item.find("date").text)
    datelist.sort()
    print (datelist)

def get_03_17_spenders(root):
    print("03/17 spenders:")
    for item in root.findall("./budget_item"):
        if ("2017-03") in item.find("date").text:
            print(item.find("name/firstname").text)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Be sure you include the relative path to the xml data input")