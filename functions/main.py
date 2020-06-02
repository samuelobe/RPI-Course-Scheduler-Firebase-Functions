import pandas as pd
import time
import csv
import json
import sys
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from collections import defaultdict


def test(request):

    project_id = 'course-scheduler-e52d1'
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': project_id,
    })

    db = firestore.client()

    start_time = time.time()

    f = open('api_key.json',) 
    data = json.load(f)
    project_id = data['project_id']
    f.close()

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
    tables = pd.read_html(url)

    for i in range(len(tables)):
        # Remove unneeded strings and replace them with blank strings
        tables[i].rename({"Unnamed: 1_level_0": "", "Unnamed: 2_level_0": "", "Unnamed: 8_level_0": "",
                          "Unnamed: 10_level_0": ""}, axis="columns", inplace=True)

        # Remove column that contains unneeded data
        tables[i] = tables[i][tables[i].columns.drop(
            list(tables[i].filter(regex='Unnamed: 12_level_1')))]
        # print(tables[i])

    # Convert table data to csv formart and add it to temp file
    df = pd.concat(table, ignore_index=True)
    df.to_csv("/tmp/data.csv", index=False)

    time.sleep(1)

    csvfile = open('/tmp/data.csv', 'r')

    # Open csvfile and convert file to a list of lists
    r = csv.reader(csvfile)
    csv_lines = list(r)
    length = len(csv_lines)

    for i in range(length):
        if i >= 2:
            if csv_lines[i][0] == '' and csv_lines[i][1] == '':
                csv_lines[i][0] = csv_lines[i-1][0]
                csv_lines[i][1] = csv_lines[i-1][1]
            elif csv_lines[i][2] == '':
                csv_lines[i][2] = 'LEC'
    # Remove the headers
    csv_lines.remove(csv_lines[0])
    csv_lines.remove(csv_lines[0])


    key_tuple = ('CRN Course-Sec', 'Course Title', 'Class Type', 'Credit Hrs', 'Gr Tp',
                  'Class Days', 'Start Time', 'End Time', 'Instructor', 'Max Enrl', 'Enrl', 'Sts Rmng')

    for line in csv_lines:
        if 'NOTE:' in line[1]:
            csv_lines.remove(line)

    courses_dict = {"courses": {}}

    for line in csv_lines:
        # If testing locally add .decode('utf8') at the end of each string
        courses_dict['courses'].setdefault(line[0].split()[1], []).append({
            key_tuple[1]: line[1],
            key_tuple[2]: line[2],
            key_tuple[3]: line[3],
            key_tuple[4]: line[4],
            key_tuple[5]: line[5],
            key_tuple[6]: line[6],
            key_tuple[7]: line[7],
            key_tuple[8]: line[8],
            key_tuple[9]: line[9],
            key_tuple[10]: line[10],
            key_tuple[11]: line[11],
        })

    # Add courses to Firestore 
    doc_ref = db.collection('courses')

    for key, values in courses_dict['courses'].items():
        doc = doc_ref.document(key).collection('class_types')
        for v in values:
            doc.document(v['Class Type']).set(v)

    # Convert Dict to JSON
    r = json.dumps(courses_dict)
    """
    test = open('data.json', 'w')
    test.write(r)
    """
    csvfile.close()
    end_time = time.time()

    # Return the JSON for testing purposes
    return r, 200, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    test('skrt')
    os.remove("/tmp/data.csv")
