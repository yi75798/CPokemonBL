#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   03_cpbl_merge.py
# Time    :   2025/12/29 21:55:58
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : CPBL 球員資料照片合併

import pandas as pd
import numpy as np

#### 讀取資料
df = pd.read_excel('cpbl_data.xlsx', sheet_name='Guardians') # 先讀富邦球員當起始
df.insert(1, 'team', 'Guardians') # 在第二欄新增隊伍欄位

df_img = pd.read_excel('cpbl_img.xlsx') # 讀取圖片資料
# 轉換成 dict 方便查找
img_dict = {}
for name, url in zip(df_img['name'], df_img['img_url']):
    img_dict[name] = url

# 看一下兩份資料前五列
df.head()
df_img.head()

#### 合併各隊球員分頁
for sheet in ['Brothers', 'TSG', 'Dragons',
              'Monkeys', 'Lions']:
              # 遍歷不同隊伍的分頁
              dfn = pd.read_excel('cpbl_data.xlsx', sheet_name=sheet)
              dfn.insert(1, 'team', sheet) # 在第二欄新增隊伍欄位

              df = pd.concat([df, dfn], axis=0, ignore_index=True)


#### 合併圖片資料
df['img_url'] = ''
for i in df.index:
    player = df.loc[i, '球員']
    if player in img_dict:
        df.loc[i, 'img_url'] = img_dict[player]
    else:
        print(f'{player} 找不到圖片')

df['img_url'].head()

#### 輸出資料
df.to_excel('cpbl_merged.xlsx', index=False)