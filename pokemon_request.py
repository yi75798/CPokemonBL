#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   pokemon_img.py
# Time    :   2025/12/30 16:52:32
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : 寶可夢資料抓取

import requests
import pandas as pd
import numpy as np
import time

#### 設定API 網址
# 寶可夢數據
data_url = 'https://pokeapi.co/api/v2/pokemon/'
# 寶可夢圖片
img_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'
# 寶可夢中文名
ch_name = 'https://pokeapi.co/api/v2/pokemon-species/'

#### 設定欄位
No = [] # 編號
Name = [] # 名稱
Name_ch = [] # 中文名
Type1 = [] # 屬性1
Type2 = [] # 屬性2
Hp = [] # HP
Atk = [] # 攻擊
Def = [] # 防禦
SA = [] # 特攻
SD = [] # 特防
Sp = [] # 速度
Img_url = [] # 圖片網址

#### 取得基礎資料
for i in range(1, 387):
    r = requests.get(data_url + str(i))
    if r.status_code != 200: # 若連線失敗則先爬下一個
        print('編號 i 出現Error')
        continue

    data = r.json() # 轉成json方便查詢
    
    No.append(data['id'])  # 儲存編號
    Name.append(data['name'].capitalize()) # 儲存名稱，將首字轉大寫

    # 取得屬性1
    Type1.append(data['types'][0]['type']['name'])
    # 取得屬性2
    try:
        Type2.append(data['types'][1]['type']['name'])
    except IndexError:
        Type2.append('None')
    
    # 取得6維
    Hp.append(data['stats'][0]['base_stat']) # 儲存HP
    Atk.append(data['stats'][1]['base_stat']) # 儲存攻擊
    Def.append(data['stats'][2]['base_stat']) # 儲存防禦
    SA.append(data['stats'][3]['base_stat']) # 儲存特攻
    SD.append(data['stats'][4]['base_stat']) # 儲存特防
    Sp.append(data['stats'][5]['base_stat']) # 儲存速度

    # 取得圖片網址
    Img_url.append(img_url + str(i) + '.png') # 儲存圖片網址

    time.sleep(0.5) # 等待0.5秒避免過度 request

#### 取得中文名
for i in range(1, 387):
    r_ch = requests.get(ch_name + str(i))

    if r_ch.status_code != 200:
        print('編號 i 出現Error')

    data_ch = r_ch.json()
    
    # 觀察json結構取得中文名
    name_ch = data_ch['names'][3]['name']
    # 儲存中文名
    Name_ch.append(name_ch)

    time.sleep(0.5) # 等待0.5秒避免過度 request

#### 建立dataframe並輸出
df = pd.DataFrame({'No': No,
                   'Name': Name,
                   'Name_ch': Name_ch,
                   'Type1': Type1,
                   'Type2': Type2,
                   'Hp': Hp,
                   'Atk': Atk,
                   'Def': Def,
                   'SA': SA,
                   'SD': SD,
                   'Sp': Sp,
                   'Img_url': Img_url})

### 檢查資料有無重複、缺漏
for i in df.index:
    for c in df.columns:
        if (pd.isna(df[c].loc[i])) or (df[c].loc[i] == ''):
            print(f'第 {i} 列 {c} 欄有缺漏')
print('沒有遺漏值')

## 檢查資料有無重複
for c in ['No', 'Name', 'Name_ch', 'Img_url']:
    if df[c].duplicated().sum() != 0:
        print(f'第 {c} 欄有重複值')
print('欄位沒有重複值')    

df.to_excel('pokemon_data.xlsx', index=False)