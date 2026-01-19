import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def radar_chart(row, col, labels):
    # row = df[df["球員"] == player_name] # 取得球員資料

    values = row[col].iloc[0].values
    values = np.append(values, values[0])

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    angles = np.append(angles, angles[0])

    fig = plt.figure(figsize=(3,3))
    ax = plt.subplot(111, polar=True)

    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3, 4])
    ax.set_yticklabels(["-3", "-2", "-1", "0", "1", "2", "3", "4"])

    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)
    
    # 固定半徑範圍
    ax.set_ylim(-3, 4) # 資料集標準分數最低約 -3，最高約 4

    # 設定刻度，只留平均值（標準分數=0）
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3, 4])
    ax.set_yticklabels(["", "", "", "avg", "", "", "", ""])
    plt.setp(ax.get_yticklabels(), color="black", alpha=0.5)

    # 加粗平均數那一圈
    theta = np.linspace(0, 2*np.pi, 360)
    ax.plot(theta, np.zeros_like(theta), linewidth=1, color="black", alpha=0.25)

    ax.plot(angles, values, linewidth=2, color="#00DB00")
    ax.fill(angles, values, alpha=0.25, color="#00DB00")

    # 美化
    ax.spines["polar"].set_visible(False)
    ax.grid(True, linewidth=0.6, alpha=0.6)

    # 轉成 base64格式讓html頁面可以顯示
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")

if __name__ == "__main__":
    df = pd.read_excel("matched_result.xlsx")
    row = df[df["球員"] == "林安可"]

    img = radar_chart(row, ["PA_std", "wOBA_std", "OBP_std", "ISO_std", "K%_std", "SB_std"],
                ["PA", "wOBA", "OBP", "ISO", "100-K%", "SB"])

