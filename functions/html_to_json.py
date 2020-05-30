import pandas as pd
import time
import csv
import json
import sys
from collections import OrderedDict

def main():
    start_time = time.time()

    open('data.csv', 'w')
    csvfile = open('data.csv', 'r')
    jsonfile = open('test.json', 'w')

    # The webpage URL whose table we want to extract
    url = sys.argv[1]

    # Assign the table data to a Pandas dataframe
    table = pd.read_html(url)

    for i in range(len(table)):
        # Remove unneeded strings and replace them with blank strings
        table[i].rename({"Unnamed: 1_level_0": "", "Unnamed: 2_level_0": "", "Unnamed: 8_level_0": "",
                         "Unnamed: 10_level_0": ""}, axis="columns", inplace=True)

        # Remove column that contains unneeded data
        table[i] = table[i][table[i].columns.drop(
            list(table[i].filter(regex='Unnamed: 12_level_1')))]

    df = pd.concat(table, ignore_index=True)
    df.to_csv("data.csv", index=False)

    time.sleep(1)

    fieldnames = ("Course-Sec CRN", "Course Title", "Class Type", "Credit Hours", "Grade Type", "Class Days",
                  "Start Time", "End Time", "Instructor", "Max Enrollment", "Seats Taken", "Seats Remaining")

    reader = csv.DictReader(csvfile, fieldnames)

    courses = {"courses": []}

    i = 0
    for row in reader:
        if i >= 2:
            sorted_row = OrderedDict(sorted(row.items(),
                                            key=lambda item: reader.fieldnames.index(item[0])))
            courses['courses'].append(sorted_row)
        i += 1

    json.dump(courses, jsonfile)

    end_time = time.time()

    print('Execution time ' + str(end_time-start_time))


if __name__ == "__main__":
    main()