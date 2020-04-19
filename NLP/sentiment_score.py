'''
import os
import re

def uncertainity(path):
    words = ['anticipate', 'risk']
    counter = {i: 0 for i in words}  # is a dictionary data structure in Python
    for fileName in os.listdir(path):
        filenameopen = os.path.join(path, fileName)

        with open(filenameopen, 'r', encoding='utf-8') as in_file:
            content = in_file.readlines()
            #content = content.split('\n')
            for word in words:
                for line in content:
                    if word in line:
                        counter[word] = counter[word] + line.count(word)
                        print(line)

                        print('***'*10)

    print(counter)
    '''
            #print(content)
            #response3 = urllib.request.urlopen(url3)

            #words: list of uncertainty words from Loughran and McDonald (2011)
            #words = [r'anticipate', r'believe', r'depend', r'fluctuate', r'indefinite',
            #r'likelihood', r'possible', r'predict', r'risk', r'uncertain']
'''
            words = ['anticipate','risk']
            counter={i:0 for i in words} # is a dictionary data structure in Python
            for elem in words:
                #print(elem)
                #print(anuj)
                for line in content:
                    print(line)
                    if elem in str(line):
                        print(line)
                        #print(line)
                        #anuj[elem] = anuj[elem] + str(line).count(elem)
                    #elements = re.findall(elem,string = str(line))
                    #if elements:
                        #print(line)
                        #print(elements)
                    #print('--'*100)
                        #for word in words:
                            #anuj[word] = anuj[word] + elements.count(word)

    '''
'''
uncertainity('/home/anuj/PycharmProjects/733/data/10-K_test')
#risk 25
#risk, 7
#risk; 1


'''

import re
import os
import pandas as pd
#filedir = '/home/anuj/PycharmProjects/733/data/10-K_test'
#master = "/home/anuj/PycharmProjects/733/cik_testplay09.csv"
master = "/home/anuj/PycharmProjects/733/cik_file10forbuzzwordtest.csv"
output_10k = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-K_clean'
output_10q = '/home/anuj/PycharmProjects/733/data_08032020/2018/10-Q_clean'
#path = 'Fake'
master_df = pd.read_csv(master)
xls = pd.ExcelFile('/home/anuj/PycharmProjects/733/LoughranMcDonald_SentimentWordLists_2018.xlsx')

#https://sraf.nd.edu/textual-analysis/resources/#LM%20Sentiment%20Word%20Lists
df_uncertain = pd.read_excel(xls, 'Uncertainty')
df_positive = pd.read_excel(xls, 'Positive')
df_negative = pd.read_excel(xls, 'Negative')

df_uncertain.columns = ['Uncertain']
df_positive.columns = ['Positive']
df_negative.columns = ['Negative']

df_uncertain.columns = ['Uncertain']

def uncertainity(output_10k,df,master_df,output_10q):

    #words = ['anticipate', 'risk']

    finallist = []
    #for fileName in os.listdir(path):
        #filenameopen = os.path.join(path, fileName)
    for i in range(master_df.shape[0]):
        counter = {i.lower(): 0 for i in df['Uncertain']}  # is a dictionary data structure in Python
        filepath = master_df.loc[i, 'path']

        filetype = master_df.loc[i, 'type']
        filename = filepath.split('/')[3]
        if filetype == '10-K':
            print('1')
            filelocation = os.path.join(output_10k, filename)
        else:
            print('2')
            filelocation = os.path.join(output_10q, filename)
        #for j in range(df.shape[0]):

        with open(filelocation, 'r', encoding='utf-8') as in_file:
            content = in_file.readlines()

            for word in df['Uncertain']:
                word = word.lower()
                #match_string = r'\b{}\w\b'.format(word)
                match_string1 = r'\b{}\b'.format(word)

                #p = re.compile('(' + match_string + '|' + match_string1 + ')')
                p = re.compile('(' + match_string1 + ')')

                for line in content:
                    matches = p.findall(line,re.IGNORECASE)

                    if (matches):
                        #print(matches)
                        counter[word] = counter[word] + len(matches)
        print(counter)
        finallist.append(counter)
        #print(finallist)
    master_df['uncertain'] = finallist
    master_df.to_csv('result_uncertain10mar.csv',index=False)

def positive_score(path,df):
    posscore = 0
    df['Positive'] = df['Positive'].apply(lambda x:x.lower())

    for fileName in os.listdir(path):
        filenameopen = os.path.join(path, fileName)

        with open(filenameopen, 'r', encoding='utf-8') as in_file:
            content = in_file.readlines()
            for word in df['Positive']:
                word = word.lower()
                match_string = r'\b{}\w\b'.format(word)
                match_string1 = r'\b{}\b'.format(word)

                p = re.compile('(' + match_string + '|' + match_string1 + ')')

                for line in content:
                    matches = p.findall(line, re.IGNORECASE)

                    if (matches):
                        print(matches)
                        posscore = posscore + len(matches)
    return posscore

def negative_score(path,df):
    negscore = 0
    df['Negative'] = df['Negative'].apply(lambda x: x.lower())

    for fileName in os.listdir(path):
        filenameopen = os.path.join(path, fileName)

        with open(filenameopen, 'r', encoding='utf-8') as in_file:
            content = in_file.readlines()
            for word in df['Negative']:
                word = word.lower()
                match_string = r'\b{}\w\b'.format(word)
                match_string1 = r'\b{}\b'.format(word)

                p = re.compile('(' + match_string + '|' + match_string1 + ')')

                for line in content:
                    matches = p.findall(line, re.IGNORECASE)

                    if (matches):
                        #print(matches)
                        negscore = negscore + len(matches)
    return negscore

def polarity_score(pos,neg):
    pol_score = (pos - neg) / ((pos + neg) + 0.000001)
    return pol_score


unc = uncertainity(output_10k,df_uncertain,master_df,output_10q)
print(unc)
#unc = uncertainity(output_10q,df_uncertain,master)
#print(unc)

#pos = positive_score(filedir,df_positive)
#print(pos)
#neg = negative_score(filedir,df_negative)
#print(neg)
#pol = polarity_score(pos,neg)
#print(pol)

#1 POST WORD MATCH{'abeyances': 0, 'almost': 2, 'alteration': 0, 'alterations': 0, 'ambiguities': 0, 'ambiguity': 0, 'ambiguous': 3, 'anomalies': 0, 'anomalous': 0, 'anomalously': 0, 'anomaly': 0, 'anticipate': 49, 'anticipated': 27, 'anticipates': 0, 'anticipating': 0, 'anticipation': 0, 'anticipations': 0, 'apparent': 2, 'apparently': 0, 'appear': 4, 'appeared': 1, 'appearing': 0, 'appears': 0, 'approximate': 19, 'approximated': 0, 'approximately': 140, 'approximates': 1, 'approximating': 0, 'approximation': 0, 'approximations': 0, 'arbitrarily': 0, 'arbitrariness': 0, 'arbitrary': 0, 'assume': 13, 'assumed': 12, 'assumes': 1, 'assuming': 6, 'assumption': 58, 'assumptions': 57, 'believe': 86, 'believed': 1, 'believes': 10, 'believing': 0, 'cautious': 0, 'cautiously': 0, 'cautiousness': 0, 'clarification': 0, 'clarifications': 0, 'conceivable': 0, 'conceivably': 0, 'conditional': 2, 'conditionally': 0, 'confuses': 0, 'confusing': 0, 'confusingly': 0, 'confusion': 0, 'contingencies': 7, 'contingency': 4, 'contingent': 13, 'contingently': 5, 'contingents': 0, 'could': 162, 'crossroad': 0, 'crossroads': 0, 'depend': 17, 'depended': 0, 'dependence': 5, 'dependencies': 0, 'dependency': 0, 'dependent': 7, 'depending': 2, 'depends': 1, 'destabilizing': 0, 'deviate': 0, 'deviated': 0, 'deviates': 0, 'deviating': 0, 'deviation': 0, 'deviations': 0, 'differ': 18, 'differed': 0, 'differing': 5, 'differs': 0, 'doubt': 0, 'doubted': 0, 'doubtful': 17, 'doubts': 0, 'exposure': 46, 'exposures': 0, 'fluctuate': 5, 'fluctuated': 0, 'fluctuates': 0, 'fluctuating': 0, 'fluctuation': 36, 'fluctuations': 36, 'hidden': 1, 'hinges': 0, 'imprecise': 0, 'imprecision': 0, 'imprecisions': 0, 'improbability': 0, 'improbable': 0, 'incompleteness': 0, 'indefinite': 55, 'indefinitely': 0, 'indefiniteness': 0, 'indeterminable': 0, 'indeterminate': 0, 'inexact': 0, 'inexactness': 0, 'instabilities': 0, 'instability': 0, 'intangible': 119, 'intangibles': 23, 'likelihood': 3, 'may': 252, 'maybe': 0, 'might': 12, 'nearly': 7, 'nonassessable': 0, 'occasionally': 0, 'ordinarily': 0, 'pending': 16, 'perhaps': 0, 'possibilities': 0, 'possibility': 4, 'possible': 15, 'possibly': 6, 'precaution': 0, 'precautionary': 0, 'precautions': 0, 'predict': 17, 'predictability': 0, 'predicted': 5, 'predicting': 0, 'prediction': 1, 'predictions': 0, 'predictive': 0, 'predictor': 0, 'predictors': 0, 'predicts': 0, 'preliminarily': 0, 'preliminary': 9, 'presumably': 0, 'presume': 0, 'presumed': 0, 'presumes': 0, 'presuming': 0, 'presumption': 0, 'presumptions': 0, 'probabilistic': 0, 'probabilities': 0, 'probability': 6, 'probable': 18, 'probably': 0, 'random': 0, 'randomize': 0, 'randomized': 0, 'randomizes': 0, 'randomizing': 0, 'randomly': 0, 'randomness': 0, 'reassess': 0, 'reassessed': 0, 'reassesses': 0, 'reassessing': 0, 'reassessment': 0, 'reassessments': 0, 'recalculate': 0, 'recalculated': 0, 'recalculates': 0, 'recalculating': 0, 'recalculation': 0, 'recalculations': 0, 'reconsider': 0, 'reconsidered': 0, 'reconsidering': 0, 'reconsiders': 0, 'reexamination': 0, 'reexamine': 0, 'reexamining': 0, 'reinterpret': 0, 'reinterpretation': 0, 'reinterpretations': 0, 'reinterpreted': 0, 'reinterpreting': 0, 'reinterprets': 0, 'revise': 4, 'revised': 1, 'risk': 136, 'risked': 0, 'riskier': 0, 'riskiest': 0, 'riskiness': 0, 'risking': 0, 'risks': 54, 'risky': 0, 'roughly': 0, 'rumors': 0, 'seems': 0, 'seldom': 0, 'seldomly': 0, 'sometime': 4, 'sometimes': 4, 'somewhat': 3, 'somewhere': 0, 'speculate': 0, 'speculated': 0, 'speculates': 0, 'speculating': 0, 'speculation': 1, 'speculations': 0, 'speculative': 9, 'speculatively': 0, 'sporadic': 0, 'sporadically': 0, 'sudden': 0, 'suddenly': 0, 'suggest': 0, 'suggested': 0, 'suggesting': 0, 'suggests': 0, 'susceptibility': 0, 'tending': 0, 'tentative': 0, 'tentatively': 0, 'turbulence': 0, 'uncertain': 21, 'uncertainly': 0, 'uncertainties': 11, 'uncertainty': 16, 'unclear': 0, 'unconfirmed': 0, 'undecided': 0, 'undefined': 0, 'undesignated': 0, 'undetectable': 0, 'undeterminable': 0, 'undetermined': 0, 'undocumented': 0, 'unexpected': 4, 'unexpectedly': 0, 'unfamiliar': 0, 'unfamiliarity': 0, 'unforecasted': 0, 'unforseen': 0, 'unguaranteed': 0, 'unhedged': 0, 'unidentifiable': 0, 'unidentified': 0, 'unknown': 1, 'unknowns': 0, 'unobservable': 13, 'unplanned': 0, 'unpredictability': 0, 'unpredictable': 0, 'unpredictably': 0, 'unpredicted': 0, 'unproved': 0, 'unproven': 0, 'unquantifiable': 0, 'unquantified': 0, 'unreconciled': 0, 'unseasonable': 0, 'unseasonably': 0, 'unsettled': 0, 'unspecific': 0, 'unspecified': 0, 'untested': 0, 'unusual': 0, 'unusually': 0, 'unwritten': 0, 'vagaries': 0, 'vague': 3, 'vaguely': 0, 'vagueness': 0, 'vaguenesses': 0, 'vaguer': 0, 'vaguest': 0, 'variability': 4, 'variable': 12, 'variables': 1, 'variably': 0, 'variance': 0, 'variances': 0, 'variant': 0, 'variants': 0, 'variation': 0, 'variations': 0, 'varied': 3, 'varies': 0, 'vary': 3, 'varying': 27, 'volatile': 2, 'volatilities': 0, 'volatility': 2}
#EXACT MATCH{'abeyances': 0, 'almost': 2, 'alteration': 0, 'alterations': 0, 'ambiguities': 0, 'ambiguity': 0, 'ambiguous': 3, 'anomalies': 0, 'anomalous': 0, 'anomalously': 0, 'anomaly': 0, 'anticipate': 22, 'anticipated': 27, 'anticipates': 0, 'anticipating': 0, 'anticipation': 0, 'anticipations': 0, 'apparent': 2, 'apparently': 0, 'appear': 4, 'appeared': 1, 'appearing': 0, 'appears': 0, 'approximate': 18, 'approximated': 0, 'approximately': 140, 'approximates': 1, 'approximating': 0, 'approximation': 0, 'approximations': 0, 'arbitrarily': 0, 'arbitrariness': 0, 'arbitrary': 0, 'assume': 0, 'assumed': 12, 'assumes': 1, 'assuming': 6, 'assumption': 1, 'assumptions': 57, 'believe': 75, 'believed': 1, 'believes': 10, 'believing': 0, 'cautious': 0, 'cautiously': 0, 'cautiousness': 0, 'clarification': 0, 'clarifications': 0, 'conceivable': 0, 'conceivably': 0, 'conditional': 2, 'conditionally': 0, 'confuses': 0, 'confusing': 0, 'confusingly': 0, 'confusion': 0, 'contingencies': 7, 'contingency': 4, 'contingent': 13, 'contingently': 5, 'contingents': 0, 'could': 162, 'crossroad': 0, 'crossroads': 0, 'depend': 16, 'depended': 0, 'dependence': 5, 'dependencies': 0, 'dependency': 0, 'dependent': 7, 'depending': 2, 'depends': 1, 'destabilizing': 0, 'deviate': 0, 'deviated': 0, 'deviates': 0, 'deviating': 0, 'deviation': 0, 'deviations': 0, 'differ': 18, 'differed': 0, 'differing': 5, 'differs': 0, 'doubt': 0, 'doubted': 0, 'doubtful': 17, 'doubts': 0, 'exposure': 46, 'exposures': 0, 'fluctuate': 5, 'fluctuated': 0, 'fluctuates': 0, 'fluctuating': 0, 'fluctuation': 0, 'fluctuations': 36, 'hidden': 1, 'hinges': 0, 'imprecise': 0, 'imprecision': 0, 'imprecisions': 0, 'improbability': 0, 'improbable': 0, 'incompleteness': 0, 'indefinite': 55, 'indefinitely': 0, 'indefiniteness': 0, 'indeterminable': 0, 'indeterminate': 0, 'inexact': 0, 'inexactness': 0, 'instabilities': 0, 'instability': 0, 'intangible': 96, 'intangibles': 23, 'likelihood': 3, 'may': 252, 'maybe': 0, 'might': 12, 'nearly': 7, 'nonassessable': 0, 'occasionally': 0, 'ordinarily': 0, 'pending': 16, 'perhaps': 0, 'possibilities': 0, 'possibility': 4, 'possible': 15, 'possibly': 6, 'precaution': 0, 'precautionary': 0, 'precautions': 0, 'predict': 17, 'predictability': 0, 'predicted': 5, 'predicting': 0, 'prediction': 1, 'predictions': 0, 'predictive': 0, 'predictor': 0, 'predictors': 0, 'predicts': 0, 'preliminarily': 0, 'preliminary': 9, 'presumably': 0, 'presume': 0, 'presumed': 0, 'presumes': 0, 'presuming': 0, 'presumption': 0, 'presumptions': 0, 'probabilistic': 0, 'probabilities': 0, 'probability': 6, 'probable': 18, 'probably': 0, 'random': 0, 'randomize': 0, 'randomized': 0, 'randomizes': 0, 'randomizing': 0, 'randomly': 0, 'randomness': 0, 'reassess': 0, 'reassessed': 0, 'reassesses': 0, 'reassessing': 0, 'reassessment': 0, 'reassessments': 0, 'recalculate': 0, 'recalculated': 0, 'recalculates': 0, 'recalculating': 0, 'recalculation': 0, 'recalculations': 0, 'reconsider': 0, 'reconsidered': 0, 'reconsidering': 0, 'reconsiders': 0, 'reexamination': 0, 'reexamine': 0, 'reexamining': 0, 'reinterpret': 0, 'reinterpretation': 0, 'reinterpretations': 0, 'reinterpreted': 0, 'reinterpreting': 0, 'reinterprets': 0, 'revise': 3, 'revised': 1, 'risk': 82, 'risked': 0, 'riskier': 0, 'riskiest': 0, 'riskiness': 0, 'risking': 0, 'risks': 54, 'risky': 0, 'roughly': 0, 'rumors': 0, 'seems': 0, 'seldom': 0, 'seldomly': 0, 'sometime': 0, 'sometimes': 4, 'somewhat': 3, 'somewhere': 0, 'speculate': 0, 'speculated': 0, 'speculates': 0, 'speculating': 0, 'speculation': 1, 'speculations': 0, 'speculative': 9, 'speculatively': 0, 'sporadic': 0, 'sporadically': 0, 'sudden': 0, 'suddenly': 0, 'suggest': 0, 'suggested': 0, 'suggesting': 0, 'suggests': 0, 'susceptibility': 0, 'tending': 0, 'tentative': 0, 'tentatively': 0, 'turbulence': 0, 'uncertain': 19, 'uncertainly': 0, 'uncertainties': 11, 'uncertainty': 16, 'unclear': 0, 'unconfirmed': 0, 'undecided': 0, 'undefined': 0, 'undesignated': 0, 'undetectable': 0, 'undeterminable': 0, 'undetermined': 0, 'undocumented': 0, 'unexpected': 4, 'unexpectedly': 0, 'unfamiliar': 0, 'unfamiliarity': 0, 'unforecasted': 0, 'unforseen': 0, 'unguaranteed': 0, 'unhedged': 0, 'unidentifiable': 0, 'unidentified': 0, 'unknown': 1, 'unknowns': 0, 'unobservable': 13, 'unplanned': 0, 'unpredictability': 0, 'unpredictable': 0, 'unpredictably': 0, 'unpredicted': 0, 'unproved': 0, 'unproven': 0, 'unquantifiable': 0, 'unquantified': 0, 'unreconciled': 0, 'unseasonable': 0, 'unseasonably': 0, 'unsettled': 0, 'unspecific': 0, 'unspecified': 0, 'untested': 0, 'unusual': 0, 'unusually': 0, 'unwritten': 0, 'vagaries': 0, 'vague': 3, 'vaguely': 0, 'vagueness': 0, 'vaguenesses': 0, 'vaguer': 0, 'vaguest': 0, 'variability': 4, 'variable': 11, 'variables': 1, 'variably': 0, 'variance': 0, 'variances': 0, 'variant': 0, 'variants': 0, 'variation': 0, 'variations': 0, 'varied': 3, 'varies': 0, 'vary': 3, 'varying': 27, 'volatile': 2, 'volatilities': 0, 'volatility': 2}