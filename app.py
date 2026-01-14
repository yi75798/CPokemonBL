#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   app.py
# Time    :   2025/12/29 21:28:53
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : 網頁程式試做

from flask import Flask, render_template, make_response, request, redirect, url_for
import pandas as pd
import os
import urllib.parse
from visualization import radar_chart

app = Flask(__name__)

#### 讀檔
BASE_DIR = os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, "matched_result.xlsx")
df = pd.read_excel(DATA_PATH)

team_name = {
    "Guardians": "富邦悍將",
    "Brothers": "中信兄弟",
    "Dragons": "味全龍",
    "Lions": "統一7-ELEVEn獅",
    "TSG": "台鋼雄鷹"
}

#### 各頁面
### 首頁
@app.route("/")
def index():
    teams = {}

    for team, group in df.groupby("team"):
        team_zh = team_name.get(team, team)  # 找不到就用原名
        teams[team_zh] = sorted(group["球員"].unique())

    return render_template("index.html", teams=teams)

@app.route("/search")
def search():
    player_name = request.args.get("q", "").strip()

    if not player_name:
        return redirect(url_for("index"))

    return redirect(f"/{urllib.parse.quote(player_name)}")


### 球員頁
@app.route('/<path:player_name>', methods=['GET']) # 球員頁
def player_page(player_name):
    # 球員姓名轉成編碼
    player_name = urllib.parse.unquote(player_name)

    row = df[df["球員"] == player_name]

    if row.empty:
        return make_response(f'查無此球員：{player_name}', 404)

    d = row.iloc[0]
    
    # 雷達圖
    player_radar = radar_chart(row,
                               ['PA_std', 'wOBA_std', 'OBP_std', 'ISO_std', 'K%_std', 'SB_std'],
                               ['PA', 'wOBA', 'OBP', 'ISO', '100-K%', 'SB'])
    pm_radar = radar_chart(row,
                           ['pm_Hp_std', 'pm_Atk_std', 'pm_Def_std', 'pm_SA_std', 'pm_SD_std', 'pm_Sp_std'],
                           ['Hp', 'Atk', 'Def', 'SA', 'SD', 'Sp'])
    

    return render_template(
        "player.html",
        ## 帶入資料
        # 球員
        player_name= d['球員'],
        player_img= d['img_url'],
        PA= d['PA'],
        wOBA= round(d['wOBA'], 3),
        OBP= round(d['OBP'], 3),
        ISOP= round(d['ISO'], 3),
        K_rate= 100-d['K%'], # K 值取（1-K%）
        SB= d['SB'],
        player_radar= player_radar,

        # 寶可夢
        pokemon_name= d['pm_Name_ch'],
        pokemon_img= d['pm_Img_url'],
        Hp= d['pm_Hp'],
        Atk= round(d['pm_Atk'], 3),
        Def= round(d['pm_Def'], 3),
        SA= round(d['pm_SA'], 3),
        SD= d['pm_SD'],
        Sp= d['pm_Sp'],
        pm_radar= pm_radar
    )

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=10000, use_reloader=False)