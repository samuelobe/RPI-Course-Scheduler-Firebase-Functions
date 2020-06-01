import pandas as pd
import time
import csv
import json
import sys
from collections import OrderedDict
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def test(request):

    project_id = 'course-scheduler-e52d1'
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': project_id,
    })

    db = firestore.client()

    start_time = time.time()

    open('/tmp/data.csv', 'w')
    csvfile = open('/tmp/data.csv', 'r')

    # The webpage URL whose table we want to extract
    url = 'https://sis.rpi.edu/reg/zs20200501.htm'

    # Assign the table data to a Pandas dataframe
    tables = pd.read_html(url)

    for i in range(len(tables)):
        # Remove unneeded strings and replace them with blank strings
        tables[i].rename({"Unnamed: 1_level_0": "", "Unnamed: 2_level_0": "", "Unnamed: 8_level_0": "",
                          "Unnamed: 10_level_0": ""}, axis="columns", inplace=True)

        # Remove column that contains unneeded data
        tables[i] = tables[i][tables[i].columns.drop(
            list(tables[i].filter(regex='Unnamed: 12_level_1')))]
        # print(tables[i])

    # Create temp .csv file
    df = pd.concat(tables, ignore_index=True)
    df.to_csv("/tmp/data.csv", index=False)

    time.sleep(1)

    r = csv.reader(open('/tmp/data.csv'))
    csv_lines = list(r)
    length = len(csv_lines)
    for i in range(length):
        if i >= 2:
            if csv_lines[i][0] == '' and csv_lines[i][1] == '':
                csv_lines[i][0] = csv_lines[i-1][0]
                csv_lines[i][1] = csv_lines[i-1][1]

    for line in csv_lines:
        if 'NOTE:' in line[1]:
            csv_lines.remove(line)

    writer = csv.writer(open('/tmp/data.csv', 'w'))
    writer.writerows(csv_lines)

    time.sleep(1)

    fieldnames = ("Course-Sec CRN", "Course Title", "Class Type", "Credit Hours", "Grade Type", "Class Days",
                  "Start Time", "End Time", "Instructor", "Max Enrollment", "Seats Taken", "Seats Remaining")

    reader = csv.DictReader(csvfile, fieldnames)

    courses = {"courses": {}}
    #f = open("test_json.json", "w")

    i = 0
    for row in reader:
        # print(row)
        # f.write(json.dumps(row))
        if i >= 2:
            sorted_row = OrderedDict(row.items())
            courses['courses'][sorted_row['Course-Sec CRN']] = sorted_row
        i += 1

    
    end_time = time.time()
    csvfile.close()
    # f.close()

    # Add courses to Firestore
    doc_ref = db.collection('courses')

    for course in courses['courses']:
        doc_ref.document(course).set(courses['courses'][course])

    courses_json = json.dumps(courses)
    return courses_json, 200, {'Content-Type': 'application/json'}

"""
if __name__ == "__main__":
    test()
"""
