#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   CPBL_crawler.py
# Time    :   2025/12/25 13:44:23
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : 中職球員數據爬蟲

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

#### 球員數據爬蟲函式
def get_table(url, wait=10, retries=3):
    '''
    url: 爬取的網址
    wait: 等待載入時間
    retries: 重試次數
    '''
    ### 先以 selenium 打開網頁，並等待頁面載入完畢
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(wait) # 設定等待載入時間

    for attempt in range(retries): # 設定若出現載入錯誤，則重試
        try:
            time.sleep(wait)  # 等待頁面載入
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            if '# 團隊進攻 ' not in soup.text:
                raise ValueError("資料尚未載入")
            
            # 成功取得 soup，跳出迴圈
            break

        except Exception as e:
            print(f"嘗試第 {attempt+1} 次失敗，延長等待時間 10 秒...")
            wait += 10
            time.sleep(10)
    else:
        driver.quit()
        raise RuntimeError("多次嘗試後仍無法載入資料")

    ## 取得第一個表格「團隊進攻」內的資料
    tables = soup.find_all("table")[1] 
    tbody = tables.find_all('tbody')

    # 取得header
    cname = tbody[0].find_all('th') 
    cname = [i.text for i in cname]

    # 建立dataframe
    df_1 = pd.DataFrame(columns=cname)

    # 取得每一個 row 的資料
    row = tbody[0].find_all('tr', {'role': 'row'})
    #row = [i.text for i in row]
    for r in range(1,len(row)):
        values = row[r].find_all('td')
        value = [td.get_text(strip=True) for td in values]
        df_1.loc[len(df_1)] = value
    
    ## 取得第二個表格「進攻成績」內的資料
    tables = soup.find_all("table")[5] 
    tbody = tables.find_all('tbody')

    # 取得header
    cname = tbody[0].find_all('th') 
    cname = [i.text for i in cname]

    # 建立dataframe
    df_2 = pd.DataFrame(columns=cname)

    # 取得每一個 row 的資料
    row = tbody[0].find_all('tr', {'role': 'row'})
    #row = [i.text for i in row]
    for r in range(1,len(row)):
        values = row[r].find_all('td')
        value = [td.get_text(strip=True) for td in values]
        df_2.loc[len(df_2)] = value
    
    return {'TO': df_1, 'OS': df_2} # 以dict形式回傳兩個dataframe

### 以球員為基準，合併兩個表的函式
def merge_table(df1, df2):
    cols_to_add = df2.columns.difference(df1.columns) # 先移除表2中與表1相同的欄位
    cols_to_add = cols_to_add.insert(0, '球員') # 加回球員欄位以供合併用
    return df1.merge(df2[cols_to_add], on='球員', how='left')

#### 六隊球員數據網址
url_bro = 'https://www.rebas.tw/tournament/CPBL-2025-JO/firstbase/Kae1X-%E4%B8%AD%E4%BF%A1%E5%85%84%E5%BC%9F'
url_tsg = 'https://www.rebas.tw/tournament/CPBL-2025-JO/firstbase/t6zJf-%E5%8F%B0%E9%8B%BC%E9%9B%84%E9%B7%B9'
url_oil = 'https://www.rebas.tw/tournament/CPBL-2025-JO/firstbase/R2VRh-%E5%91%B3%E5%85%A8%E9%BE%8D'
url_monkeys = 'https://www.rebas.tw/tournament/CPBL-2025-JO/firstbase/WyADE-%E6%A8%82%E5%A4%A9%E6%A1%83%E7%8C%BF'
url_lions = 'https://www.rebas.tw/tournament/CPBL-2025-JO/firstbase/Xs1sP-%E7%B5%B1%E4%B8%807-ELEVEn%E7%8D%85'
url_fb = 'https://www.rebas.tw/tournament/CPBL-2025-JO/firstbase/wi4T3-%E5%AF%8C%E9%82%A6%E6%82%8D%E5%B0%87'

#### 開始六隊球員數據爬蟲
tables_bro = get_table(url_bro)
table_tsg = get_table(url_tsg)
table_oil = get_table(url_oil)
table_monkeys = get_table(url_monkeys)
table_lions = get_table(url_lions)
table_fb = get_table(url_fb)

#### 合併六隊各兩個表，並儲存成 xlsx 檔
bro = merge_table(tables_bro['TO'], tables_bro['OS'])
tsg = merge_table(table_tsg['TO'], table_tsg['OS'])
oil = merge_table(table_oil['TO'], table_oil['OS'])
monkeys = merge_table(table_monkeys['TO'], table_monkeys['OS'])
lions = merge_table(table_lions['TO'], table_lions['OS'])
fb = merge_table(table_fb['TO'], table_fb['OS'])

with pd.ExcelWriter("cpbl_data.xlsx") as writer:
    bro.to_excel(writer, sheet_name='Brothers', index=False)
    tsg.to_excel(writer, sheet_name='TSG', index=False)
    oil.to_excel(writer, sheet_name='Dragons', index=False)
    monkeys.to_excel(writer, sheet_name='Monkeys', index=False)
    lions.to_excel(writer, sheet_name='Lions', index=False)
    fb.to_excel(writer, sheet_name='Guardians', index=False)
    