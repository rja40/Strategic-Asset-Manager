{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sqlalchemy import create_engine\n",
    "from yahoofinancials import YahooFinancials\n",
    "from datetime import date"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "\n",
    "data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')\n",
    "table = data[0]\n",
    "\n",
    "table1 = table[1:]\n",
    "\n",
    "sp_list = table1[['Symbol','Security','GICS Sector','CIK']]\n",
    "sp_list = sp_list.rename(columns={'Symbol': 'symbol', 'Security': 'company_name','GICS Sector': 'sector','CIK' : 'cik'})\n",
    "\n",
    "engine = create_engine('postgresql://postgres:postgres@localhost:5432/stocks')\n",
    "sp_list.to_sql('company_info', con=engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "engine = create_engine('postgresql://postgres:postgres@localhost:5432/stocks')\n",
    "df = pd.read_sql_query('select symbol,company_name from \"company_info\"',con=engine)\n",
    "\n",
    "symbols = df['symbol'].tolist()\n",
    "yahoo_financials_tech = YahooFinancials(symbols)\n",
    "\n",
    "daily_stocks_prices = yahoo_financials_tech.get_historical_price_data('2010-01-01',str(date.today()), 'daily')\n",
    "for symbol in symbols:\n",
    "    try:\n",
    "        prices_list = daily_stocks_prices.get(symbol).get(\"prices\")\n",
    "        df_prices = pd.DataFrame.from_dict(prices_list)\n",
    "        df_prices = df_prices[['high','low','open','close','volume','formatted_date']]\n",
    "        subsetDataFrame = df[df['symbol'] == symbol]\n",
    "        company_name = subsetDataFrame['company_name']\n",
    "        df_prices['year'] = pd.to_datetime(df_prices['formatted_date']).dt.year\n",
    "        df_prices['company_name'] = company_name.values[0]\n",
    "        df_prices['symbol'] = symbol\n",
    "        df_prices.to_sql('stocks_prices', con=engine,if_exists='append',index=False)\n",
    "    except:\n",
    "        pass\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
