import streamlit as st

from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

from pydantic import BaseModel
import pandas as pd

def crop_image(image, crop_box):
    cropped_image = image.crop(crop_box)
    return cropped_image


import json

class CSV(BaseModel):
    resume_csv: str
    vacancy_csv: str

class Resume(BaseModel):
    job: str = ""
    url: str = ""
    number: str = ''


# Функция для отображения списка кастомных объектов
def display_custom_item(custom_item: Resume):
    st.write(f"# [{custom_item['job']}]({custom_item['url']})")
    # st.write(f"{custom_item['url']}")
    st.subheader(f"Соответствие: {(1 - float(custom_item['number'])) * 100 :.2f} %")
    st.write("---")


@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def init():
    # primaryColor="#9C73F8"


    st.set_page_config(
        page_title="hh.ru analyzer",
        layout="wide",
        initial_sidebar_state="expanded")

    st.markdown("""
    <style>
    .big-font {
        font-size:80px !important;
    }
    </style>
    """, unsafe_allow_html=True)


    # 9C73F8

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False


def page1(selected):
    if selected == "Главная":
        # Header
        st.title("hh.ru analyzer")
        st.subheader('*Система для автоматического анализа резюме кандидатов*')



        st.divider()

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.header('Как это работает?')
                st.markdown(
                    """
                    - Загрузите вакансию: Просто загрузите описание вакансии, и наш алгоритм сделает остальное.

                    - Анализируем резюме: Наша система анализирует резюме кандидатов, чтобы определить их соответствие вашим требованиям.

                    - Выбирайте лучшие варианты: Получите список релевантных кандидатов и выберите наиболее подходящих для вашей компании.
                    """
                )
            with col2:
                lottie2 = load_lottiefile("static/analyze_lottie.json")
                st_lottie(lottie2, key='place', height=300, width=300)

        st.divider()


def page2(selected):
    # Search Page
    if selected == "Рейтинг кандидатов":
        st.header('Рейтинг кандидатов')
        st.divider()
        items = []

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Загрузите csv с вакансией')

                uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type=["csv"])



                if uploaded_file is not None:

                    try:
                        vacancy = pd.read_csv(uploaded_file)
                        vac = {'vacancy': vacancy.text[0]}


                        req = requests.post(url="http://127.0.0.1:8000/api/v1/model_server/kneighbors", json=vac)

                        items = req.json()
                        st.write(vacancy.text[0])

                    except Exception as e:
                        st.warning(e, icon="⚠️")
                    with col2:
                        try:
                            with st.container(height=646):

                                for item in items:
                                    display_custom_item(item)

                        except Exception as e:
                            print(e)


def page3(selected):
    # Search Page
    if selected == "Анализ соответствия":
        st.header('Анализ соответствия')
        st.divider()

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Загрузите csv с вакансией')

                uploaded_file_vacancy = st.file_uploader("Choose a vacancy", accept_multiple_files=False, type=["csv"])

                if uploaded_file_vacancy is not None:

                    try:
                        vacancy = pd.read_csv(uploaded_file_vacancy)

                    except Exception as e:
                        st.warning(e, icon="⚠️")
            with col2:
                st.subheader('Загрузите csv с резюме')

                uploaded_file_resume = st.file_uploader("Choose a resume", accept_multiple_files=False, type=["csv"])

                if uploaded_file_resume is not None:

                    try:
                        resume = pd.read_csv(uploaded_file_resume)

                    except Exception as e:
                        st.warning(e, icon="⚠️")

            if st.button("Check similiar"):
                try:
                    data = {"resume_csv": resume.text[0],
                            "vacancy_csv": vacancy.text[0]
                            }


                    # Serialize the data to JSON bytes
                    req = requests.post(url="http://127.0.0.1:8000/api/v1/model_server/predict_item", json=data)

                except Exception as e:
                    st.warning(e, icon="⚠️")
                st.header(f"Процент схожести:{req.text.strip('"')} %")



def page4(selected):
    # Search Page
    if selected == "О нас":
        st.subheader('Создатели')
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Олег")
            st.image('static/images/image1.jpg', caption='Sunrise by the mountains')
        with col2:
            st.subheader("Богдан")
            st.image('static/images/image1.jpg', caption='Sunrise by the mountains',)
        with col3:
            st.subheader("Марсель")

            st.image('static/images/image3.jpg', caption='Sunrise by the mountains')
        with col4:
            st.subheader("Данил")
            st.image('static/images/image4.jpg', caption='Sunrise by the mountains')


def menu():
    init()
    # Options Menu
    with st.sidebar:
        selected = option_menu('Меню', ["Главная", 'Рейтинг кандидатов', 'Анализ соответствия', 'О нас'],
                               icons=['house', 'trophy', 'yin-yang', 'info-circle'], menu_icon='intersect', default_index=0)
    page1(selected)
    page2(selected)
    page3(selected)
    # page4(selected)


if __name__ == "__main__":
    menu()
