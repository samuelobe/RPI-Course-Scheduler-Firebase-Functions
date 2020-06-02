import pandas as pd
import time
import csv
import json
import sys
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def test(request):
    start_time = time.time()

    project_id = 'course-scheduler-e52d1'
    # Use the application default credentials
    #cred = credentials.ApplicationDefault()
    cred = credentials.Certificate(
        "api_key.json")

    firebase_admin.initialize_app(cred, {
        'projectId': project_id,
    })

    db = firestore.client()

    # Create temp file for GCP

    csvfile = open('/tmp/data.csv', 'w')

    # The webpage URL whose table we want to extract
    url = 'https://sis.rpi.edu/reg/zs20200501.htm'

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
    df.to_csv("/tmp/data.csv", index=False)

    time.sleep(1)

    csvfile = open('/tmp/data.csv', 'r')

    r = csv.reader(csvfile)
    csv_lines = list(r)
    length = len(csv_lines)

    for i in range(length):
        if i >= 2:
            if csv_lines[i][0] == '' and csv_lines[i][1] == '':
                csv_lines[i][0] = csv_lines[i-1][0]
                csv_lines[i][1] = csv_lines[i-1][1]

    csv_lines.remove(csv_lines[0])
    csv_lines.remove(csv_lines[0])

    dict_tuple = ('CRN Course-Sec', 'Course Title', 'Class Type', 'Credit Hrs', 'Gr Tp',
                  'Class Days', 'Start Time', 'End Time', 'Instructor', 'Max Enrl', 'Enrl', 'Sts Rmng')

    for line in csv_lines:
        if 'NOTE:' in line[1]:
            csv_lines.remove(line)

    courses = {"courses": {}}

    for line in csv_lines:
        courses['courses'][line[0].split()[1].decode('utf8')] = {
            dict_tuple[1].decode('utf8'): line[1].decode('utf8'),
            dict_tuple[2].decode('utf8'): line[2].decode('utf8'),
            dict_tuple[3].decode('utf8'): line[3].decode('utf8'),
            dict_tuple[4].decode('utf8'): line[4].decode('utf8'),
            dict_tuple[5].decode('utf8'): line[5].decode('utf8'),
            dict_tuple[6].decode('utf8'): line[6].decode('utf8'),
            dict_tuple[7].decode('utf8'): line[7].decode('utf8'),
            dict_tuple[8].decode('utf8'): line[8].decode('utf8'),
            dict_tuple[9].decode('utf8'): line[9].decode('utf8'),
            dict_tuple[10].decode('utf8'): line[10].decode('utf8'),
            dict_tuple[11].decode('utf8'): line[11].decode('utf8'),
        }

    # Add courses to Firestore
    doc_ref = db.collection('courses')

    for course in courses['courses']:
        doc_ref.document(course).set(courses['courses'][course])

    """
    r = json.dumps(courses)
    test = open('data.json', 'w')
    test.write(r)
    """

    csvfile.close()
    end_time = time.time()
    return r, 200, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    test('skrt')
    os.remove("/tmp/data.csv")
