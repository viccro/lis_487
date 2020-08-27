#!/usr/local/bin/python3

import sys
import csv
import re
import pprint as pp

def main(csv_path):
    with open(csv_path, newline='') as input_file:
        filereader = csv.DictReader(input_file, fieldnames=['name','email','category','price','date'])
        category_totals = dict()
        monthly_totals = dict()

        for row in filereader:
            category = row['category']
            amount = float(row['price'].strip('$'))
            date = row['date']
            month = re.sub("\d+-(\d+)-\d+",
                           "\g<1>",
                           date)

            category_totals[category] = round(category_totals.get(category, 0) + amount, 2)
            monthly_totals[month] = round(monthly_totals.get(month, 0) + amount, 2)

    print("Category Totals:")
    pp.pprint(category_totals)
    print("\nHighest spending in: ", max(category_totals, key=category_totals.get),"\n")

    print("Monthly Totals: ")
    pp.pprint(monthly_totals)
    print("\nHighest spending in: ", max(monthly_totals, key=monthly_totals.get),"\n")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Be sure you include the relative path to the csv data input")