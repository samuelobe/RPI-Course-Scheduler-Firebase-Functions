import pandas as pd
import time

start_time = time.time()
# The webpage URL whose table we want to extract
url = "https://sis.rpi.edu/reg/zs20200501.htm"

# Assign the table data to a Pandas dataframe
table = pd.read_html(url)

for i in range(len(table)):
    print('\n')
    # Remove unneeded strings and replace them with blank strings
    table[i].rename({"Unnamed: 1_level_0": "", "Unnamed: 2_level_0": "", "Unnamed: 8_level_0": "",
                     "Unnamed: 10_level_0": ""}, axis="columns", inplace=True)

    # Remove column that contains unneeded data
    table[i] = table[i][table[i].columns.drop(
        list(table[i].filter(regex='Unnamed: 12_level_1')))]

    print(table[i])

df = pd.concat(table, ignore_index=True)
df.to_csv("data.csv", index=False)

end_time = time.time()

print('Execution time', end_time-start_time)
