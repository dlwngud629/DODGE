import sqlite3
import os

def insert_images_from_folder(db_path, folder_path):
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 폴더 내 모든 파일에 대해 반복
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):  # 이미지 파일 형식 확인
            file_path = os.path.join(folder_path, filename)
            champion_name = os.path.splitext(filename)[0]

            # 이미지 파일 읽기
            with open(file_path, 'rb') as f:
                img = f.read()

            # 데이터베이스에 이미지 데이터 삽입
            cursor.execute("INSERT OR REPLACE INTO image (champion, data) VALUES (?, ?)", (champion_name, img))

    conn.commit()
    conn.close()

# 데이터베이스 파일 경로와 이미지 폴더 경로 설정
database_path = 'C:/Users/ace/Desktop/DODGE/lol.db'
image_folder_path = 'C:/Users/ace/Desktop/DODGE/champs'

# 함수 실행
insert_images_from_folder(database_path, image_folder_path)
