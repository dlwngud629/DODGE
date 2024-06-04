import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image
import io
from PIL import ImageOps

def get_db_connection():
    return sqlite3.connect('lol.db')

def add_border(img, border_size=5, color='blue'):
    # 이미지에 테두리를 추가하는 함수
    width, height = img.size
    new_width = width + 2*border_size
    new_height = height + 2*border_size
    new_img = Image.new("RGB", (new_width, new_height), color)
    new_img.paste(img, (border_size, border_size))
    return new_img

def get_champion_image(champion_name, conn, size=(64, 64), border_color='blue'):
    query = "SELECT data FROM image WHERE champion = ?"
    result = pd.read_sql(query, conn, params=(champion_name,))
    if not result.empty:
        image_data = result.iloc[0]['data']
        image = Image.open(io.BytesIO(image_data))
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)  # 이미지 크기 조정
        image = add_border(image, border_size=5, color=border_color)  # 테두리 추가
        return image
    else:
        print(f"Image not found for champion: {champion_name}")
        default_image = Image.open("path_to_default_image.jpg")
        default_image = ImageOps.fit(default_image, size, Image.Resampling.LANCZOS)
        default_image = add_border(default_image, border_size=5, color=border_color)
        return default_image




def id_page(summoner_name):
    conn = get_db_connection()
    try:
        puuid_query = "SELECT PUUID FROM summoners_puuid WHERE SummonerName = ?"
        puuid_result = pd.read_sql(puuid_query, conn, params=(summoner_name,))
        if not puuid_result.empty:
            puuid = puuid_result.iloc[0]['PUUID']
            matches_query = """
            SELECT UserChampion, BlueTeamChampions, RedTeamChampions, WinningTeam 
            FROM sorted_matches_info 
            WHERE PUUID = ?
            """
            matches = pd.read_sql(matches_query, conn, params=(puuid,))
            st.header(f"소환사 명: {summoner_name}")
            
            for index, match in matches.iterrows():
                blue_champs = match['BlueTeamChampions'].split(', ')
                red_champs = match['RedTeamChampions'].split(', ')
                
                # 이미지 크기를 통일
                blue_images = [get_champion_image(champ, conn, size=(64, 64), border_color='blue') for champ in blue_champs]
                red_images = [get_champion_image(champ, conn, size=(64, 64), border_color='red') for champ in red_champs]

                # UserChampion의 팀 색상 결정
                user_champ = match['UserChampion']
                if user_champ in blue_champs:
                    user_team_color = 'blue'
                elif user_champ in red_champs:
                    user_team_color = 'red'
                else:
                    user_team_color = 'gray'  

                user_image = get_champion_image(user_champ, conn, size=(64, 64), border_color=user_team_color)

                # 승리 여부에 따른 이모지 추가
                if user_team_color == match['WinningTeam'].lower():
                    champion_display = f"👑 {match['UserChampion']}"
                else:
                    champion_display = f"😢 {match['UserChampion']}"

                st.markdown("---")
                col1, col2, col3, col4 = st.columns([0.4, 1, 0.15, 1.11])
                col1.image(user_image, width=50)
                col1.write(champion_display)

                col2.image(blue_images, width=50)

                col3.subheader("VS")

                col4.image(red_images, width=50)
        else:
            st.header("No data found for the given Summoner Name.")
    finally:
        conn.close()
