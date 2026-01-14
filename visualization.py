#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   08_visualization.py
# Time    :   2026/01/13 16:16:37
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description :

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

# df = pd.read_excel('matched_result.xlsx')

# players_col = ['PA_std', 'wOBA_std', 'OBP_std', 'ISO_std', 'K%_std', 'SB_std']
# players_labels = ['PA', 'wOBA', 'OBP', 'ISO', '100-K%', 'SB']

# pm_col = ['pm_Hp_std', 'pm_Atk_std', 'pm_Def_std', 'pm_SA_std', 'pm_SD_std', 'pm_Sp_std']
# pm_labels = ['Hp', 'Atk', 'Def', 'SA', 'SD', 'Sp']

def radar_chart(row, col, labels):
    # row = df[df['球員'] == player_name]
    
    values = row[col].iloc[0].values
    values = np.append(values, values[0])  # 封閉雷達圖

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    angles = np.append(angles, angles[0])

    fig = plt.figure(figsize=(3,3))
    ax = plt.subplot(111, polar=True)

    # ax.plot(angles, values, linewidth=2, color="#00DB00")
    # ax.fill(angles, values, alpha=0.25, color="#00DB00")

    ax.set_ylim(-3, 4) # 固定半徑

    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3, 4])
    ax.set_yticklabels(["-3", "-2", "-1", "0", "1", "2", "3", "4"])

    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)
    
    # === 固定半徑範圍 ===
    ax.set_ylim(-3, 4)

    # === 刻度（你可以自由調整）===
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3, 4])
    ax.set_yticklabels(["", "", "", "avg", "", "", "", ""])
    plt.setp(ax.get_yticklabels(), color='black', alpha=0.5)

    # === 加粗 0 那一圈 ===
    theta = np.linspace(0, 2*np.pi, 360)
    ax.plot(theta, np.zeros_like(theta), linewidth=1, color='black', alpha=0.25)

    ax.plot(angles, values, linewidth=2, color="#00DB00")
    ax.fill(angles, values, alpha=0.25, color="#00DB00")

    # === 美化 ===
    ax.spines["polar"].set_visible(False)
    ax.grid(True, linewidth=0.6, alpha=0.6)

    # ⭐ 關鍵：轉成 base64
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")

if __name__ == "__main__":
    df = pd.read_excel("matched_result.xlsx")
    row = df[df["球員"] == "林安可"]

    img = radar_chart(row, ['PA_std', 'wOBA_std', 'OBP_std', 'ISO_std', 'K%_std', 'SB_std'],
                ['PA', 'wOBA', 'OBP', 'ISO', '100-K%', 'SB'])

