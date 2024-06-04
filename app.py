import streamlit as st
import dodge
import datacrud
from id import id_page  # Import the id_page function from id.py

def app():
    st.set_page_config(page_title="DOTG")

    # 로고
    st.markdown("<h2 style='text-align: center; font-size: 10em;'>. G<br></h2>", unsafe_allow_html=True)
    st.markdown("***")

    # 아이디 입력을 위한 텍스트 필드
    user_id = st.text_input("아이디를 입력하세요", key='user_id')
    

    # CSS 스타일 추가
    st.markdown(
        """
        <style>
        .button-style {
            width: 100%;
            height: 50px;  /* 높이도 원하는 대로 설정할 수 있습니다 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 두 개의 컬럼 생성, 동일한 비율로 설정
    col1, col2 = st.columns([1, 1])

    # 첫 번째 컬럼에 첫 번째 버튼 추가
    with col1:
        if st.button("DODGE 추천", key="dodge_button"):
            st.session_state.page = 'dodge'
            st.experimental_rerun()

    # 두 번째 컬럼에 두 번째 버튼 추가
    with col2:
        if st.button("데이터 수정", key="data_crud_button"):
            st.session_state.page = 'datacrud'
            st.experimental_rerun()

    # 버튼 스타일 적용
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
)


    # 사용자가 텍스트 필드에 입력을 하면 page 상태를 'id'로 설정
    if user_id:
        st.session_state.page = 'id'
        st.experimental_rerun()

if 'page' not in st.session_state:
    st.session_state.page = 'app'

if st.session_state.page == 'app':
    app()
elif st.session_state.page == 'dodge':
    dodge.dodge()
elif st.session_state.page == 'datacrud':
    datacrud.datacrud()
elif st.session_state.page == 'id':
    if 'user_id' in st.session_state:
        id_page(st.session_state.user_id)

