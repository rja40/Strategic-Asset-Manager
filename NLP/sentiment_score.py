import re
import os
import pandas as pd
from collections import Counter 
import collections
import time

print("pid is")
print(os.getpid())
#filedir = '/home/asus/Downloads/NLP/10K-QFiles'
master = "cikfile_0704.csv"
cleaned_10k = '/home/akundra/scratch/bigdata/files/10-K_cleaned'
cleaned_10q = '/home/akundra/scratch/bigdata/files/10-Q_cleaned'
master_df = pd.read_csv(master)
xls = pd.ExcelFile('LoughranMcDonald_SentimentWordLists_2018.xlsx')

#https://sraf.nd.edu/textual-analysis/resources/#LM%20Sentiment%20Word%20Lists
df = pd.read_excel(xls, 'Uncertainty')
df.columns = ['uncertainity']
df['positive'] = pd.read_excel(xls, 'Positive')
df['negative'] = pd.read_excel(xls, 'Negative')

def positive_score(filename):
    posscore = 0
    print("calculating positive score")
    df['positive'] = df['positive'].apply(lambda x:x.lower())

    for word in df['positive'].tolist():
        match_string = r'\b{}\b'.format(word)
        words = re.findall(match_string, open(filename).read())
        if(words):
            posscore = posscore + len(words)
    return posscore

def negative_score(filename):
    negscore = 0
    print("calculating negative score ")
    df['negative'] = df['negative'].apply(lambda x: x.lower())
    for word in df['negative'].tolist():
        match_string = r'\b{}\b'.format(word)
        words = re.findall(match_string, open(filename).read())
        if(words):
            negscore = negscore + len(words)
    return negscore

def polarity_score(pos,neg):
    pol_score = (pos - neg) / ((pos + neg) + 0.000001)
    return pol_score


def uncertainity():

    finallist_dict = []
    sum_uncertain_values = []
    postive_score_values = []
    negative_score_values = []
    polarity_score_values = []
    
    
    for i in range(master_df.shape[0]):
        print(i)
        file_word_dict = dict()
        
        word_list = [item.lower() for item in df['uncertainity'].tolist()]
        cnt = Counter()
        for word in word_list :
            cnt[word] += 0
            
        filepath = master_df.loc[i, 'path']
        filetype = master_df.loc[i, 'type']
        filename = filepath.split('/')[3]
        
        if filetype == '10-K':
            print("Processing 10-K file")
            file_absolute_path = os.path.join(cleaned_10k, filename)
        else:
            print("Processing 10-Q file")
            file_absolute_path = os.path.join(cleaned_10q, filename)
        
        print(file_absolute_path)    
        for word in word_list:
            match_string = r'\b{}\b'.format(word)
            words = re.findall(match_string, open(file_absolute_path).read())
            word_dict = dict(collections.Counter(words))
            file_word_dict = {**file_word_dict,**word_dict}
               
        print("here")
        finallist_dict.append(file_word_dict)
        
        sum_dict_values = sum(file_word_dict.values())
        print(sum_dict_values)
        sum_uncertain_values.append(sum_dict_values)
        
        positive_value = positive_score(file_absolute_path)
        print(positive_value)
        postive_score_values.append(positive_value)
        
        negative_value = negative_score(file_absolute_path)
        print(negative_value)
        negative_score_values.append(negative_value)
        
        polarity_score_value = polarity_score(positive_value,negative_value)
        print(polarity_score_value)
        polarity_score_values.append(polarity_score_value)
    
    master_df['uncertainity_words'] = finallist_dict
    master_df['uncertainity_score'] = sum_uncertain_values
    master_df['positive_score'] = postive_score_values
    master_df['negative_score'] = negative_score_values
    master_df['polarity_score'] = polarity_score_values
    
    print(master_df.head())
    
    master_df.to_csv('sentiment_score_0704.csv',index=False)

t0 = time.time()           
uncertainity()
print("time is")
print(int(time.time()-t0))
