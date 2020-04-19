# Strategic Asset Manager

## Introduction
The project forecasts company's stocks price taking into account its historical performance, sentimental analysis on Edgar reports, legal proceeding sections and sentimental anaylsis on global news concerning the companies.
This repo presents code in 3 module given below:

## Set up
#### Libraries and Requirements

* Pandas
* Numpy
* Beautiful Soup
* Keras
* Scikit-Learn
* PostgreSQL
* SQLAlchemy
* Matplotlib
* AWScli
* NLTK
* Gensim
* Boto3
* Paramiko

#### Edgar reports scrapping and Sentimental analysis
NLP

 * filegen.py - create a CSV file which contains all the information on edgar reports including 10-K and 10-Q.
 * bulkdl.py - this file downloads all the Edgar reports provided in the cik master csv file. 
 * clean_rawfile.py - cleans all the edgar reports provided in the csv file by removing all the html tags.
 * sentiment_score.py - create a csv file by running sentiments analysis on all the clean files created from edgar reports
 * similarity_legalproceedings.ipynb - extract the legal proceedings section from Edgar reports and calculate the similarity index
 *  


#### Machine Learning Prediction
 
 * prediction_meanprice_sentiment.py - builds and train the models for 35 companies mentioned in the ticker. 
 * prediction_90days.py -  forecasts 90 days values from the models created
 * mutual_funds.py - builds and train the models for top mutuals funds
 
#### Chatbot

