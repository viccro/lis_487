#!/usr/local/bin/python3

import sys
import re
import csv
from datetime import date, datetime

def main(csv_path):
    with open(csv_path, newline='') as input_file, open("tmp.txt", 'w') as output_file:
        filereader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=['id','birthday','weight','height','bmi'])
        writer.writeheader()

        for row in filereader:
            date = standardize_date(row['birthday'])
            weight = clean_weights(row['weight'])
            height = convert_height(row['height'])
            bmi = calculate_bmi(weight, height)
            writer.writerow({'id': row['id'],
                             'birthday':date,
                             'weight':weight,
                             'height':height,
                             'bmi':bmi})

    with open("tmp.txt", newline='') as output_csv:
        filereader = csv.DictReader(output_csv)
        analyze_stats(filereader)

def standardize_date(date):
    if re.match("\d\d[\\\/\-\– \|]+\d\d[\\\/\-\– \|]+\d\d\d\d", date):      #MM/DD/YYYY
        return re.sub("(\d\d)[\\\/\-\– \|]+(\d\d)[\\\/\-\– \|]+(\d\d\d\d)",
               "\g<3>-\g<1>-\g<2>",
               date)
    elif re.match("\d[\\\/\-\– \|]+\d\d[\\\/\-\– \|]+\d\d\d\d", date):
        return re.sub("(\d)[\\\/\-\– \|]+(\d\d)[\\\/\-\– \|]+(\d\d\d\d)",
                      "\g<3>-0\g<1>-\g<2>",
                      date)

def clean_weights(weight):
    return re.sub("\D*(\d)\D*",
                  "\g<1>",
                  weight)

def convert_height(height):
    foot_str = re.sub("(\d) ?\' ?\d?.*",
                  "\g<1>",
                  height)
    inch_str = re.sub("\d ?\' ?(\d)?.*",
                  "\g<1>",
                  height)
    if not inch_str:
        inch_str = 0
    return foot_and_in_to_total_inches(foot_str, inch_str, height)

def foot_and_in_to_total_inches(foot_str, inch_str, height):
    total_inches = int(foot_str)*12 + int(inch_str)
    return str(total_inches)

def calculate_bmi(weight, height):
    w = int(weight)
    h = int(height)
    bmi = 703 * w / (h * h)
    return bmi

def analyze_stats(filereader):
    min_age = 1000
    max_age = 0
    total_age = 0
    min_height = 1000
    max_height = 0
    total_height = 0
    min_bmi = 1000
    max_bmi = 0
    total_bmi = 0
    total_rows = 0

    for row in filereader:
        age = calculate_age_in_days(row['birthday'])
        if age < min_age:
            min_age = age
        if age > max_age:
            max_age = age
        total_age += age

        height = int(row['height'])
        if height < min_height:
            min_height = height
        if height > max_height:
            max_height = height
        total_height += height

        bmi = float(row['bmi'])
        if bmi < min_bmi:
            min_bmi = bmi
        if bmi > max_bmi:
            max_bmi = bmi
        total_bmi += bmi

        total_rows += 1

    average_age = total_age / total_rows
    average_height = total_height / total_rows
    average_bmi = total_bmi / total_rows

    with open("output.txt", 'a') as output_file:
        output_file.write("Min age: "+str(min_age)+" days\n")
        output_file.write("Max age: "+str(max_age)+" days\n")
        output_file.write("Average age: "+str(average_age)+" days\n")

        output_file.write("Min height: "+str(min_height)+" inches\n")
        output_file.write("Max height: "+str(max_height)+" inches\n")
        output_file.write("Average height: "+str(average_height)+" inches\n")

        output_file.write("Min bmi: "+str(min_bmi)+"\n")
        output_file.write("Max bmi: "+str(max_bmi)+"\n")
        output_file.write("Averave bmi: "+str(average_bmi))



def calculate_age_in_days(birthday):
    birthday_obj = datetime.strptime(birthday, '%Y-%m-%d')
    today_obj = datetime.today()
    age = today_obj - birthday_obj
    age_in_days = age.days
    return age_in_days

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Be sure you include the relative path to the csv data input")