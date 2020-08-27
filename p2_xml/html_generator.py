#!/usr/local/bin/python3

import sys
import csv

html_out = "output.html"
html_preamble_and_header = """<!DOCTYPE html>
<html>
    <head>
        <title>Henry V: Entire Play</title>
    </head>
    <body>
"""

table_open = """        <table style="width:100%">
            <tr>
                <th>Date</th>
                <th>Category</th>
                <th>Amount</th>
            </tr>
"""
table_close = """</table>"""

def main(csv_path):
    html_file = html_preamble_and_header + table_open
    with open(csv_path, newline='') as input_file:
        filereader = csv.DictReader(input_file, fieldnames=['name','email','category','price','date'])

        for row in filereader:
            html_file += create_html_table_row(row, ['date','category','price'])

    html_file += table_close

    with open(html_out, 'w') as writer:
        writer.write(html_file)

def create_html_table_row(row, list_of_columns):
    table_row = "<tr>\n"
    for col in list_of_columns:
        table_row += "<td>"+row[col]+"</td>\n"
    table_row += "</tr>\n"
    return table_row

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Be sure you include the relative path to the csv data input")