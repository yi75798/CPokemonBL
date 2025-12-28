#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   CPBL_img_crawler.py
# Time    :   2025/12/26 23:57:45
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : 中職球員頭像爬蟲

import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

#### 先進入網頁
session = requests.Session() # 建立 session

url = 'https://cpbl.com.tw/team?ClubNo=AEO' # 以富邦球員頁面為入口
resp = session.get(url, verify=False) # 取得網頁

soup = BeautifulSoup(resp.text, 'html.parser') # 解析網頁

#### 取得 JS 所需要的資料
'''
因為球員頁面是在 JavaScript 中產生，所以需要先取得 token, header, data 等需要發送的資料
才能讓頁面出現需要的 html
'''

### 取得 token
token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

### 設定 header
headers = {
    'User-Agent': 'Mozilla/5.0',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://cpbl.com.tw/team?ClubNo=AEO'
}

### 設定 data
## 所需球隊、一二軍球隊的資料都是藉由 data 參數控制，所以寫成函式
def get_data(Club, Kind):
    '''
    Club: 球隊代碼
    kind: 一二軍
    '''
    data = {
            '__RequestVerificationToken': token,
            'ClubNo': Club,
            'KindCode': Kind
           }
    return data

#### 送出 post, 取得 html，並存在 list 中
## 建立球隊對應代碼
# AEO=邦邦, AJL=吱吱, ACN=爪爪, ADD=喵喵, AAA=油龍, AKP=啾啾
club_code = {'fb': 'AEO',
        'monkeys': 'AJL',
        'bro': 'ACN',
        'lions': 'ADD',
        'oil': 'AAA',
        'tsg': 'AKP'}

## 建立 list 準備儲存資料
team = []
html_lst = []

## 開始取得資料
for club in club_code: 
    for kind in ['A', 'D']: # A 一軍，D 二軍
        resp = session.post(
            "https://cpbl.com.tw/team",
            headers=headers,
            data= get_data(club_code[club], kind) # 帶入data參數
        )
        team.append(club) # 儲存球隊
        html_lst.append(resp.text) # 儲存html
        time.sleep(3) # 間隔 3 秒

# 將抓到的資料整理成 dataframe
html_lst = pd.DataFrame({'team':team, 'html':html_lst})

#### 從抓到的 html 中取得圖片網址
# 準備容器儲存資料
name = []
team_name = []
img_url = []

## 遍歷 html_lst中取得抓到的html及對應的球隊
for html, Team in zip(html_lst['html'], html_lst['team']):
    html = BeautifulSoup(html, 'html.parser')
    html = html.find_all('a')

    for a in html:
        try:
            target = a['style'] # 如果是球員（<a style...），則取得html內容
            # 用 regex 取得圖片網址
            match = re.search(r"url\(['\"]?(.*?)['\"]?\)", target)
            # 取得球員名稱並去除特殊字元
            Name = re.sub(r"[*@#◎]", "", a.text)
            # 儲存資料進前面準備好的容器
            name.append(Name)
            img_url.append('https://cpbl.com.tw/' + match.group(1))
            team_name.append(Team)
        except:
            # 出問題表示該html不是對應到球員，因此略過
            continue

## 整理成 dataframe
img_data = pd.DataFrame({'name':name, 'team':team_name, 'img_url':img_url})

#### 輸出資料
img_data.to_excel('cpbl_img.xlsx', index=False)
