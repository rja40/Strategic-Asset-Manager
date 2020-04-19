import urllib.request as urllib2
import pandas as pd
import re
import os
#string_match1 = 'edgar/data/1018724/0001193125-13-028520.txt'
#file = "cik_testplay09.csv"
file = "/home/anuj/PycharmProjects/733/cik_file10forbuzzwordtest.csv"
df = pd.read_csv(file)
path_10k = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-K'
path_10q = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-Q'
for i in range(df.shape[0]):
    filepath = df.loc[i,'path']
    filetype = df.loc[i,'type']
    filename = filepath.split('/')[3]
    filename = filename.split('$\n')[0]
    print(filename)
    if filetype == '10-K':
        filelocation = os.path.join(path_10k, filename)
        print(filelocation)
    else:
        filelocation = os.path.join(path_10q,filename)
        print(filelocation)


    url = 'https://www.sec.gov/Archives/'+ filepath
    with open(filelocation, "w",encoding='utf-8') as file:
        datarequest = urllib2.urlopen(url)
        data = datarequest.read()
        text = data.decode('utf-8')
        file.write(text)


'''
data = open(file, "r")
for line in data:
    if re.match(r"^\d+.*$", line):
        path = line.split(',')[3]
        print(line)
        print(path)
        print('--')

'''
'''
url3 = 'https://www.sec.gov/Archives/'+string_match1
#load the page in for the given url in response3
#urllib2 is a Python module that can be used for fetching URLs
with open('/data/10-K/check1.txt', "wb") as file:
    response3 = urllib2.urlopen(url3)
    data = response3.read()
    #text = data.decode('utf-8')
    file.write(data)
'''