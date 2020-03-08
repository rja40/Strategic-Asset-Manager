import os
import re
import pandas as pd

def rawdata_extract(path, cikListFile, output):
    html_regex = re.compile(r'<.*?>')  # HTML TAGS

    cikListFile = pd.read_csv(cikListFile)
    for index, row in cikListFile.iterrows():
        processingFile = row['path'].split('/')

        inputFile = processingFile[3]

        for fileName in os.listdir(path):
            filenameopen = os.path.join(path, fileName)
            filenamewrite = os.path.join(output, fileName)
            currentFile = fileName

            if os.path.isfile(filenameopen) and currentFile == inputFile:

                with open(filenameopen, 'r', encoding='utf-8', errors="replace") as in_file:
                    content = in_file.read()

                    content = re.sub(html_regex, '', content)  # Deleting <....> HTML tags by replacing with ''
                    content = content.replace('&nbsp;', '')  # Deleting Breaking Space
                    content = re.sub(r'&#\d+;', '', content)  # Deleting &#9477 type of things

                with open(filenamewrite, 'w') as out_file:
                    out_file.write(content)

                in_file.close()
                out_file.close()

inputDirectory = '/home/anuj/PycharmProjects/733/data/10-K'
masterFile = '/home/anuj/PycharmProjects/733/cik2018_test.csv'
outputDirectory = '/home/anuj/PycharmProjects/733/data/10-K_clean'
rawdata_extract( inputDirectory , masterFile, outputDirectory )


