#!/usr/bin/env python
# coding: utf-8

# In[37]:


import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import Any, Dict
import pandas as pd


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_profile(stock: Any) -> Dict[str, Any]:
    
    url = f'https://finance.yahoo.com/quote/{stock}/profile'
    
    r = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(r.text, 'html')
    
    name = soup.find('h1', class_ = 'D(ib) Fz(18px)').text

    address = soup.find('p', class_ = 'D(ib) W(47.727%) Pend(40px)').text

    execs = soup.find_all('td', class_ = 'Ta(start)')

    exec1 = execs[0].text
    exec2 = execs[2].text
    exec3 = execs[4].text
    exec4 = execs[6].text
    exec5 = execs[8].text

    description = soup.find('p', class_ = 'Mt(15px) Lh(1.6)').text

    governance = soup.find('p', class_ = 'Fz(s)').text
    
    stock = {'name': name, 'address': address, 'exec1': exec1, 'exec2': exec2, 'exec3': exec3, 'exec4': exec4,
             'exec5': exec5, 'description': description, 'governance': governance}
    
    print(stock)
    return stock
    

ticker_symbols = ['TSLA', 'AMZN', 'AAPL', 'META', 'NFLX', 'GOOG']

stockdata = [get_profile(symbol) for symbol in ticker_symbols]

with open('Rini_stock_profile_data.json', 'w', encoding='utf-8') as f: json.dump(stockdata, f)

CSV_FILE_PATH = 'Rini_stock_profile_data.csv'
with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = stockdata[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore') 
    writer.writeheader()
    writer.writerows(stockdata)

EXCEL_FILE_PATH = 'Rini_stock_profile_data.xlsx'
df = pd.DataFrame(stockdata) 
df.to_excel(EXCEL_FILE_PATH, index=False)

print('Done!')
    

