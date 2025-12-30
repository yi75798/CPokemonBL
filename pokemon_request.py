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
data_url = 'https://pokeapi.co/api/v2/pokemon/'
img_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'

#### 設定欄位
No = [] # 編號
Name = [] # 名稱
Type1 = [] # 屬性1
Type2 = [] # 屬性2
Hp = [] # HP
Atk = [] # 攻擊
Def = [] # 防禦
SA = [] # 特攻
SD = [] # 特防
Sp = [] # 速度
Img_url = [] # 圖片網址

#### 開始取得資料
for i in range(1, 387):
    r = requests.get(data_url + str(i))
    if r.status_code != 200:
        print('編號 i 出現Error')
        continue

    data = r.json()
    
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

#### 建立dataframe並輸出
df = pd.DataFrame({'No': No,
                   'Name': Name,
                   'Type1': Type1,
                   'Type2': Type2,
                   'Hp': Hp,
                   'Atk': Atk,
                   'Def': Def,
                   'SA': SA,
                   'SD': SD,
                   'Sp': Sp,
                   'Img_url': Img_url})

df.to_excel('pokemon_data.xlsx', index=False)