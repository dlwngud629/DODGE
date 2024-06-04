import streamlit as st
import sqlite3
import base64
from PIL import Image
import io

champions = [
    'Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe',
    'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Briar', 'Caitlyn', 'Camille',
    'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'DrMundo', 'Draven', 'Ekko', 'Elise', 'Evelynn',
    'Ezreal', 'FiddleSticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves',
    'Gwen', 'Hecarim', 'Heimerdinger', 'Hwei', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax',
    'Jayce', 'Jhin', 'Jinx', 'KSante', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina',
    'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'Leblanc', 'LeeSin', 'Leona',
    'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'Milio',
    'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Naafiri', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee',
    'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana',
    'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble',
    'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed',
    'Sion', 'Sivir', 'Skarner', 'Smolder', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench',
    'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch',
    'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor',
    'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi',
    'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra'
]
# 데이터베이스 연결 함수
def get_database_connection():
    return sqlite3.connect('lol.db')

# 챔피언 이미지를 데이터베이스에서 가져오는 함수
def get_champion_image(conn, champion_name):
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM image WHERE champion = ?", (champion_name,))
    result = cursor.fetchone()
    if result:
        image_data = result[0]
        img = Image.open(io.BytesIO(image_data))
        img = img.resize((250, 282))  # 이미지 크기 조정
        return img
    else:
        return None


# 챔피언 선택 및 데이터베이스 조회
def dodge():
    victory = st.text_input("Victory point reward")
    defeat = st.text_input("Defeat point reward")
    selected_champions = st.multiselect('Select 5 Champions:', champions, help="Select exactly 5 champions for querying the database.")
    if len(selected_champions) == 5:
        formatted_champions = ", ".join(sorted(selected_champions))
        conn = get_database_connection()
        cursor = conn.cursor()
        query = f"""
        SELECT COUNT(*) as match_count,
               SUM(CASE WHEN WinningTeam = 'Blue' AND BlueTeamChampions = '{formatted_champions}' THEN 1
                         WHEN WinningTeam = 'Red' AND RedTeamChampions = '{formatted_champions}' THEN 1
                         ELSE 0 END) as wins
        FROM sorted_matches_info
        WHERE BlueTeamChampions = '{formatted_champions}' OR RedTeamChampions = '{formatted_champions}';
        """
        cursor.execute(query)
        result = cursor.fetchone()
        
        # 선택된 챔피언 이미지 출력
        images = [get_champion_image(conn, champ) for champ in selected_champions]
        conn.close()
        
        if result:
            match_count = result[0] if result[0] is not None else 0
            wins = result[1] if result[1] is not None else 0

            
            #st.write("ex) DODGE!!: AurelionSol, KSante, LeeSin, Sett, DODGE: Smolder	Keep Going!!: Fiora, Kaisa, Maokai, Nautilus, Yone")

            # 이미지 표시
            cols = st.columns(len(images))
            for col, img, champ in zip(cols, images, selected_champions):
                col.image(img, width=100, caption=champ)

            st.write(f"Match Count: {match_count}")
            st.write(f"Wins: {wins}")

            if wins / (match_count + 0.001) > 0.5:
                st.header("Keep Going!!")
                point = (int(victory) * int(wins) + int(defeat) * (int(match_count)-int(wins))) / int(match_count)
                st.subheader(f"You will get {int(point)} points")
            elif wins == 0 and match_count == 0:
                st.header("No Match Data!!")
            else:
                st.header("DODGE!")
                point = (int(victory) * int(wins) + int(defeat) * (int(match_count)-int(wins))) / int(match_count)
                st.subheader(f"You will lose {int(point)} points")

        else:
            st.error("No data found for the selected champions.")
    elif selected_champions:
        st.warning('Please select exactly 5 champions.')

if __name__ == "__main__":
    dodge()