#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   pokemon_standardize.py
# Time    :   2025/12/31 20:16:49
# Author  :   Henry Shih 
# Email:   
# Description : 寶可夢數據標準化

import pandas as pd

# 設定路徑名稱
input_file = "pokemon_data.xlsx"     # ← 換成你的檔名
output_file = "std_pokemon_data.xlsx"

# 讀取 Excel
df = pd.read_excel(input_file)

# 要標準化的欄位（對應 E～J）
stat_cols = ["Hp", "Atk", "Def", "SA", "SD", "Sp"]

def zscore_to_01(series):
    return (series - series.mean()) / series.std()

# 逐欄處理並新增欄位
for col in stat_cols:
    df[f"{col}_std"] = zscore_to_01(df[col])

# 輸出新檔案
df.to_excel(output_file, index=False)

print("完成！已輸出標準化後的檔案：", output_file)