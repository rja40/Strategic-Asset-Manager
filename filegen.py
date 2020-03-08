import re
import pandas as pd

fin_data = []
files = ['master_2018Q1.idx','master_2018Q2.idx','master_2018Q3.idx','master_2018Q4.idx']
for file in files:
    data = open(file, "r")
    for line in data:
        my_dict = {}
        if re.match(r"^\d+.*$",line):
            type = str(line.split('|')[2])

            if (type == '10-K'):
                print(line)
                my_dict['cik'] = line.split('|')[0]
                my_dict['company'] = line.split('|')[1]
                my_dict['date'] = line.split('|')[3]
                my_dict['path'] = line.split('|')[4]

                fin_data.append(my_dict)

        else:
            continue
df = pd.DataFrame(fin_data)
df.to_csv('cik2018.csv', sep=',', encoding='utf-8',index=False)