#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   07_cluster.py
# Time    :   2026/01/05 19:33:21
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : 球員寶可夢分群

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.optimize import linear_sum_assignment

#### 讀取資料
cpbl = pd.read_excel('std_cpbl.xlsx')
pm = pd.read_excel('std_pokemon.xlsx')
# 挑選需要的欄位
cpbl = cpbl[['球員', 'team',
             'PA',
             'wOBA',
             'OBP',
             'ISO',
             'K%',
             'SB',
             'PA_std',
             'wOBA_std',
             'OBP_std',
             'ISO_std',
             'K%_std',
             'SB_std',
             'img_url']]

pm = pm[['No', 'Name_ch', 
         'Hp',
         'Atk',
         'Def',
         'SA',
         'SD',
         'Sp',
         'Hp_std',
         'Atk_std',
         'Def_std',
         'SA_std',
         'SD_std',
         'Sp_std',
         'Img_url']]

#### 分群
###  Hungarian Algorithm
## 挑出所需變項
cols_cpbl = ['PA_std',
             'wOBA_std',
             'OBP_std',
             'ISO_std',
             'K%_std',
             'SB_std']

cols_pm   = ['Hp_std',
             'Atk_std',
             'Def_std',
             'SA_std',
             'SD_std',
             'Sp_std']

# 轉換資料型態
df_cpbl = cpbl[cols_cpbl].to_numpy(float)
df_pm = pm[cols_pm].to_numpy(float)

## cost[i, j] = 建立成本矩陣表示球員 i 與 寶可夢 j 的距離
# 先將 6 維的向量轉換成 1 維
# 再沿著轉換後的6維向量計算歐氏距離
cost = np.linalg.norm(df_cpbl[:, None, :] - df_pm[None, :, :], axis=2)

# 從成本矩陣中配對使得每個 i, j只用一次，且  cost[i, j]加總最小
row_ind, col_ind = linear_sum_assignment(cost)

# 併回原資料
pm_matched = (
    pm.iloc[col_ind]
      .add_prefix('pm_')
      .reset_index(drop=True)
)

cpbl_matched = (
    cpbl.iloc[row_ind]
        .reset_index(drop=True)
)

final_df = pd.concat([cpbl_matched, pm_matched], axis=1)
# 併回每組配對的距離
final_df['dist'] = cost[row_ind, col_ind]

# 新增一欄加總寶可夢6維的「種族值總和」
final_df['stat'] = final_df['pm_Hp'] + final_df['pm_Atk'] + final_df['pm_Def'] + final_df['pm_SA'] + final_df['pm_SD'] + final_df['pm_Sp']

## 輸出
final_df.to_excel('matched_result.xlsx', index=False, sheet_name='Hungarian')