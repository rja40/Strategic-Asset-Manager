import re
import pandas as pd
from datetime import datetime
cik_value = [1800,1551152,1467373,796343,1578845,899051,1652044,1652044,764180,1018724,4962,5272,732717,318154,
             320193,70858,1390777,1067983,875045,1364742,12927,1075531,14272,927628,18230,1091667,93410,858877,
             831001,21344,21665,1166691,1163165,909832,64803,313616,1751788,1326160,1666700,32604,1109357,34088,
             1326801,1048911,37996,40533,40545,1467858,882095,886982,354950,773840,50863,51143,200406,19617,1506307,
             1637459,59478,936468,60667,1141391,63908,1613103,310158,1099219,789019,1103982,895421,1065280,753308,
             320187,1045810,797468,1341439,1633917,77476,78003,1413329,80424,804328,1047122,87347,1063761,92122,829224,
             27419,97476,97745,36104,100885,731766,1090727,101829,732712,1403161,104169,1618921,1001039,72971]
fin_data = []
files = ['master_2017Q1.idx','master_2017Q2.idx','master_2017Q3.idx','master_2017Q4.idx',
         'master_2018Q1.idx','master_2018Q2.idx','master_2018Q3.idx','master_2018Q4.idx',
         'master_2019Q1.idx','master_2019Q2.idx','master_2019Q3.idx','master_2019Q4.idx']
for file in files:
    data = open(file,'r',encoding='ISO-8859-1')
    for line in data:
        my_dict = {}
        if re.match(r"^\d+.*$",line):
            type = str(line.split('|')[2])

            if (type == '10-K' or type == '10-Q'):
                #print(line)
                company_cik = int(line.split('|')[0])
                if company_cik in cik_value:
                    my_dict['cik'] = company_cik
                    my_dict['company'] = line.split('|')[1]
                    my_dict['type'] = line.split('|')[2]
                    my_dict['date'] = line.split('|')[3]
                    dateobj = my_dict['date']

                    good_date = datetime.strptime(dateobj, '%Y-%m-%d')
                    year = good_date.year
                    month = good_date.month
                    if month >= 1 and month <= 3:
                        q = 1
                    elif month >= 4 and month <= 6:
                        q = 2
                    elif month >= 7 and month <= 9:
                        q = 3
                    else:
                        q = 4
                    quarter = 'Q' + str(q)
                    my_dict['year'] = year

                    my_dict['quarter'] = quarter

                    testpath = line.split('|')[4]
                    testpath = testpath.split('\n')[0]
                    my_dict['path'] = testpath
                    fin_data.append(my_dict)
                    print(my_dict)

        else:
            continue
print(fin_data)
df = pd.DataFrame(fin_data)
df = df.sort_values(by=['cik'])
df.to_csv('cikfile_10.csv', sep=',', encoding='utf-8',index=False)
