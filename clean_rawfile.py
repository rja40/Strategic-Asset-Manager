import os
import re
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

only_div_tags = SoupStrainer("div")


def rawdata_extract(path, cikListFile, output,typecheck):
    html_regex = re.compile(r'<.*?>')  # HTML TAGS
    stop_words = set(stopwords.words('english'))
    cikListFile = pd.read_csv(cikListFile)
    for index, row in cikListFile.iterrows():
        processingFile = row['path'].split('/')
        type = row['type']
        if type == typecheck:
            inputFile = processingFile[3].split('\n')[0]
            #for fileName in os.listdir(path):
            filenameopen = os.path.join(path, inputFile)
            filenamewrite = os.path.join(output, inputFile)
            #currentFile = fileName

            print(filenameopen)
            print(filenamewrite)

            if os.path.isfile(filenameopen):# and currentFile == inputFile
                print('IN')


                with open(filenameopen, 'r', encoding='utf-8', errors="replace") as in_file:
                    content = in_file.read()

                #soup = BeautifulSoup(open(filenameopen), "html.parser", parse_only=only_div_tags)

                    content = re.sub(html_regex, '', content)  # Deleting <....> HTML tags by replacing with ''
                    content = content.replace('&nbsp;', '')  # Deleting Breaking Space
                    content = content.replace('&gt;', '')
                    content = content.replace('&lt;', '')
                    #content = content.replace("<style([\\s\\S]+?)</style>", "")
                    content = re.sub(r'&#\d+;', '', content)  # Deleting &#9477 type of things
                    content = content.lower() #Lower case all

                    word_tokens = word_tokenize(content)
                    filtered_sentence = ' '.join([word for word in word_tokens if word not in stop_words])

                    with open(filenamewrite, 'w') as out_file:
                        out_file.write(filtered_sentence)
                '''
                with open(filenamewrite, 'w') as out_file:
                    for text in soup:
                        text = text.get_text().lower()
                        word_tokens = word_tokenize(text)
                        filtered_sentence = ' '.join([word for word in word_tokens if word not in stop_words])
                        out_file.write(filtered_sentence)
                '''

                    #in_file.close()
                    #out_file.close()

path_10k = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-K'
path_10q = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-Q'
output_10k = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-K_clean'
output_10q = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-Q_clean'
#masterfile = '/home/anuj/PycharmProjects/733/cik_testplay09.csv'
masterfile = "/home/anuj/PycharmProjects/733/cik_file10forbuzzwordtest.csv"
type10k = '10-K'
type10q = '10-Q'

rawdata_extract(path_10k , masterfile, output_10k,type10k)
rawdata_extract(path_10q , masterfile, output_10q,type10q)


