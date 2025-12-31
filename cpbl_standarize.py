#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   cpbl_standarize.py
# Time    :   2025/12/31 16:50:05
# Author  :   Henry Shih 
# Email:   
# Description : 中職球員數據標準化

import pandas as pd

# 設定路徑名稱
input_file = "edit_cpbl_PA120_players.xlsx" # ← 改成你的檔名
output_file = "std_cpbl_PA120_players.xlsx" # 輸出檔名

# 讀取 Excel
df = pd.read_excel(input_file)

# 第 2～7 欄對應的欄位名稱
cols_normal = ["PA", "wOBA", "OBP", "ISO", "SB"]
col_k = "K%" # K% 特殊處理

def zscore_to_01(series):
    return (series - series.mean()) / series.std()

# 一般欄位
for col in cols_normal:
    df[f"{col}_std"] = zscore_to_01(df[col])

# K% 特殊處理
k_percent = df[col_k] / 100        # 百分化
k_reversed = 1 - k_percent         # 反轉，因K%越低表示表現越好
df[f"{col_k}_std"] = zscore_to_01(k_reversed)


# 輸出
df.to_excel(output_file, index=False)

print("完成！已輸出檔案：", output_file)