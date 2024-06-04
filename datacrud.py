import base64
import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import io

def show_summoner_data(conn):
    st.subheader("Summoner Table")
    query_summoners = "SELECT * FROM summoners_puuid"
    data_summoners = pd.read_sql_query(query_summoners, conn)
    st.dataframe(data_summoners, height=400)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='color:blue;'>Insert Summoner Data</h4>", unsafe_allow_html=True)
        new_puuid = st.text_input("Enter PUUID", key="puuid_summoner")
        new_summoner = st.text_input("Enter Summoner Name", key="summoner_name")
        if st.button("Insert Summoner"):
            conn.execute("INSERT INTO summoners_puuid (PUUID, SummonerName) VALUES (?, ?)", (new_puuid, new_summoner))
            conn.commit()
            st.success("Summoner added successfully!")
            st.experimental_rerun()
    with col2:
        st.markdown("<h4 style='color:red;'>Delete Summoner Data</h4>", unsafe_allow_html=True)
        delete_puuid = st.text_input("Enter PUUID to Delete", key="delete_puuid_summoner")
        if st.button("Delete Summoner"):
            conn.execute("DELETE FROM summoners_puuid WHERE PUUID = ?", (delete_puuid,))
            conn.commit()
            st.success("Summoner deleted successfully!")
            st.experimental_rerun()
    with col3:
        st.markdown("<h4 style='color:orange;'>Update Summoner Data</h4>", unsafe_allow_html=True)
        update_puuid = st.text_input("Enter PUUID to Update", key="update_puuid")
        updated_name = st.text_input("Enter New Summoner Name", key="update_name")
        if st.button("Update Summoner"):
            conn.execute("UPDATE summoners_puuid SET SummonerName = ? WHERE PUUID = ?", (updated_name, update_puuid))
            conn.commit()
            st.success("Summoner updated successfully!")
            st.experimental_rerun()

def show_match_data(conn):
    st.subheader("Match Table")
    query_matches = "SELECT * FROM sorted_matches_info"
    data_matches = pd.read_sql_query(query_matches, conn)
    st.dataframe(data_matches, height=400)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='color:blue;'>Insert Match Data</h4>", unsafe_allow_html=True)
        new_puuid_match = st.text_input("Enter PUUID", key="puuid_match")
        new_game_id = st.text_input("Enter Game ID", key="game_id")
        new_blue_team = st.text_input("Enter Blue Team Champions", key="blue_team")
        new_red_team = st.text_input("Enter Red Team Champions", key="red_team")
        new_winning_team = st.text_input("Enter Winning Team", key="winning_team")
        new_user_champion = st.text_input("Enter User Champion", key="user_champion")  # New field for User Champion
        if st.button("Insert Match"):
            conn.execute(
                "INSERT INTO sorted_matches_info (PUUID, GameID, BlueTeamChampions, RedTeamChampions, WinningTeam, UserChampion) VALUES (?, ?, ?, ?, ?, ?)",
                (new_puuid_match, new_game_id, new_blue_team, new_red_team, new_winning_team, new_user_champion)
            )
            conn.commit()
            st.success("Match added successfully!")
            st.experimental_rerun()
    with col2:
        st.markdown("<h4 style='color:red;'>Delete Match Data</h4>", unsafe_allow_html=True)
        delete_game_id = st.text_input("Enter Game ID to Delete", key="delete_game_id")
        if st.button("Delete Match"):
            conn.execute("DELETE FROM sorted_matches_info WHERE GameID = ?", (delete_game_id,))
            conn.commit()
            st.success("Match deleted successfully!")
            st.experimental_rerun()
    with col3:
        st.markdown("<h4 style='color:orange;'>Update Match Data</h4>", unsafe_allow_html=True)
        update_game_id = st.text_input("Enter Game ID to Update", key="update_game_id")
        updated_blue_team = st.text_input("Enter Updated Blue Team Champions", key="update_blue_team")
        updated_red_team = st.text_input("Enter Updated Red Team Champions", key="update_red_team")
        updated_winning_team = st.text_input("Enter New Winning Team", key="update_winning_team")
        updated_user_champion = st.text_input("Enter Updated User Champion", key="update_user_champion")  # New field for updating User Champion
        if st.button("Update Match"):
            conn.execute(
                "UPDATE sorted_matches_info SET BlueTeamChampions = ?, RedTeamChampions = ?, WinningTeam = ?, UserChampion = ? WHERE GameID = ?",
                (updated_blue_team, updated_red_team, updated_winning_team, updated_user_champion, update_game_id)
            )
            conn.commit()
            st.success("Match updated successfully!")
            st.experimental_rerun()

def show_image_data(conn):
    st.subheader("Image Table")
    query_images = "SELECT * FROM image"
    data_images = pd.read_sql_query(query_images, conn)

    def convert_image_data_to_html(image_data):
        if image_data:
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            return f"<img src='data:image/png;base64,{image_base64}' width='60'/>"
        return ""
    col1, col2= st.columns(2)
    with col1:
        data_images['data'] = data_images['data'].apply(convert_image_data_to_html)
        st.write(data_images.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    with col2:
 
        st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:blue;'>Insert Image Data</h4>", unsafe_allow_html=True)
        new_champion = st.text_input("Enter Champion Name", key="champion_name")
        new_image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="image_file")
        if st.button("Insert Image"):
            if new_image_file is not None:
                image = Image.open(new_image_file)
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='PNG')
                image_data = image_bytes.getvalue()
                conn.execute("INSERT INTO image (champion, data) VALUES (?, ?)", (new_champion, image_data))
                conn.commit()
                st.success("Image added successfully!")
                st.experimental_rerun()

        st.markdown("<h4 style='color:red;'>Delete Image Data</h4>", unsafe_allow_html=True)
        delete_champion = st.text_input("Enter Champion Name to Delete", key="delete_champion")
        if st.button("Delete Image"):
            conn.execute("DELETE FROM image WHERE champion = ?", (delete_champion,))
            conn.commit()
            st.success("Image deleted successfully!")
            st.experimental_rerun()
        st.markdown("<h4 style='color:orange;'>Update Image Data</h4>", unsafe_allow_html=True)
        update_champion = st.text_input("Enter Champion Name to Update", key="update_champion")
        updated_image_file = st.file_uploader("Upload New Image", type=["png", "jpg", "jpeg"], key="update_image_file")
        if st.button("Update Image"):
            if updated_image_file is not None:
                updated_image = Image.open(updated_image_file)
                updated_image_bytes = io.BytesIO()
                updated_image.save(updated_image_bytes, format='PNG')
                updated_image_data = updated_image_bytes.getvalue()
                conn.execute("UPDATE image SET data = ? WHERE champion = ?", (updated_image_data, update_champion))
                conn.commit()
                st.success("Image updated successfully!")
                st.experimental_rerun()

def datacrud():
    st.sidebar.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
        font-weight: bold;
    }
    </style>
    <div class='big-font'>Select Table</div>
    """, unsafe_allow_html=True)

    option = st.sidebar.selectbox('', ('Summoner Data', 'Match Data', 'Image Data'))

    st.sidebar.write("Table Create Statement")

    create_summoners_puuid_table = """
    CREATE TABLE "summonerPuuid" (
        "SummonerName"    TEXT,
        "PUUID"    TEXT,
        PRIMARY KEY("PUUID")
    )
    """

    create_sorted_matches_info_table = """
    CREATE TABLE "matchesInfo" (
        "PUUID"    TEXT,
        "GameID"    TEXT,
        "BlueTeamChampions"    TEXT,
        "RedTeamChampions"    TEXT,
        "WinningTeam"    TEXT,
        "UserChampion"    TEXT
    )
    """

    create_image_table = """
    CREATE TABLE "image" (
        "champion"    TEXT PRIMARY KEY,
        "data"    BLOB NOT NULL
    )
    """

    st.sidebar.code(create_summoners_puuid_table, language='sql')
    st.sidebar.code(create_sorted_matches_info_table, language='sql')
    st.sidebar.code(create_image_table, language='sql')

    conn = sqlite3.connect('lol.db')

    if option == 'Summoner Data':
        show_summoner_data(conn)
    elif option == 'Match Data':
        show_match_data(conn)
    elif option == 'Image Data':
        show_image_data(conn)

    conn.close()

if __name__ == "__main__":
    datacrud()
