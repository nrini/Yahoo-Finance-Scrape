#!/usr/bin/env python
# coding: utf-8

# In[42]:


import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import Any, Dict
import pandas as pd


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_holders(stock: Any) -> Dict[str, Any]:
    
    url = f'https://finance.yahoo.com/quote/{stock}/holders'
    
    r = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(r.text, 'html')
    
    holders = soup.find_all('td', class_ = 'Py(10px) Va(m) Fw(600) W(15%)')
    
    inst = soup.find_all('td', class_ = "Ta(start) Pend(10px)")
    
    stock = {'ticker_name': stock, 'pct_shares_all_insider': holders[0].text, 'pct_shares_institutions': holders[1].text,
            'pct_float_institutions': holders[2].text, 'num_institutions_holding': holders[3].text,
            'top_institute_holder1': inst[0].text, 'top_institute_holder2': inst[1].text,
            'top_institute_holder3': inst[2].text, 'top_institute_holder4': inst[3].text,
            'top_institute_holder5': inst[4].text}
    
    print(stock)
    return stock
    

ticker_symbols = ['TSLA', 'AMZN', 'AAPL', 'META', 'NFLX', 'GOOG']

stockdata = [get_holders(symbol) for symbol in ticker_symbols]

with open('Rini_stock_holder_data.json', 'w', encoding='utf-8') as f: json.dump(stockdata, f)

CSV_FILE_PATH = 'Rini_stock_holder_data.csv'
with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = stockdata[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore') 
    writer.writeheader()
    writer.writerows(stockdata)

EXCEL_FILE_PATH = 'Rini_stock_holder_data.xlsx'
df = pd.DataFrame(stockdata) 
df.to_excel(EXCEL_FILE_PATH, index=False)

print('Done!')
    
    

