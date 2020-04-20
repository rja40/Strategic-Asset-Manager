# Strategic Asset Manager

## Introduction
The project forecasts company's stocks price taking into account its historical performance, sentimental analysis on Edgar reports, legal proceeding sections and sentimental anaylsis on global news concerning the companies.

This repo presents code in 4 module given below:

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
* Dash

#### Edgar reports scrapping and Sentimental analysis
##### NLP

 * `filegen.py` - creates a CSV file which contains all the information on edgar reports including 10-K and 10-Q
 * `bulkdl.py` - downloads all the Edgar reports provided in the cik master csv file
 * `clean_rawfile.py` - cleans all the edgar reports provided in the csv file by removing all the html tags
 * `sentiment_score.py` - creates a csv file by running sentiments analysis on all the clean files created from edgar reports
 * `similarity_legalproceedings.ipynb` - extracts the legal proceedings section from Edgar reports and calculate the similarity index from all its previous years files


#### Machine Learning Prediction
##### ml_prediction
 
 * `prediction_meanprice_sentiment.py` - builds and trains LSTM models for 35 companies mentioned in the ticker
 * `prediction_90_days.py` -  forecasts 90 days values from the models created
 * `mutualfund_data.ipynb` - creates data(csv file) for the top mutual funds
 * `mutual_funds.py` - builds and trains LSTM for the top mutuals funds

#### Chatbot
##### chatbot

* `lambda_function.py` - 

#### News

##### news
 * `sentiment_analysis_news.ipynb` - 
 * `bigquery.py` - 
 
Remaining files in the assets and pages are related to the web UI created for this project

#### Running Instructions

`python3 index.py` - to run the application 

