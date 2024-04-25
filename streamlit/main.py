# import streamlit as st
#
# from streamlit_option_menu import option_menu
# from streamlit_lottie import st_lottie
# # from code_editor import code_editor
#
# import pandas as pd
#
# import torch
#
# from model.infer import load_model, infer_model
#
# import json
#
# from sklearn.neighbors import NearestNeighbors
# from sentence_transformers import SentenceTransformer, util
# import numpy as np
#
# # Создание объекта ближайших соседей
# k = 15  # количество ближайших соседей
# nbrs = NearestNeighbors(n_neighbors=k, metric='cosine')
#
#
# class CustomItem:
#     def __init__(self, text, link, number):
#         self.text = text
#         self.link = link
#         self.number = number
#
#
# # Функция для отображения списка кастомных объектов
# def display_custom_item(custom_item):
#     st.subheader(f"Текст: {custom_item.text}")
#     st.text(f"Ссылка: [{custom_item.link}]({custom_item.link})")
#     st.text(f"Число: {custom_item.number}")
#     st.write("---")
#
#
# @st.cache_data
# def load_lottiefile(filepath: str):
#     with open(filepath, "r") as f:
#         return json.load(f)
#
#
# data, model, means = load_model()
#
# embendings = torch.load("streamlit_bert/static/embendings.pt") - (means['mean_resume'].values)
# # torch.save(embendings, 'embendings.pt')
# nbrs.fit(embendings)
#
#
# def find_nearest_neighbors(vacancy):
#     print(type(vacancy))
#     vacancy = vacancy[vacancy.find(":"):]
#     distances, indices = nbrs.kneighbors([model.encode(vacancy) - (means['mean_vac'].values)])
#     nearest_neighbors = [(data.iloc[idx], dist) for idx, dist in zip(indices[0], distances[0])]
#
#     return nearest_neighbors, indices
#
#
# def init():
#     # primaryColor="#9C73F8"
#
#     st.set_page_config(
#         page_title="hh.ru analyzer",
#         layout="wide",
#         initial_sidebar_state="expanded")
#
#     st.markdown("""
#     <style>
#     .big-font {
#         font-size:80px !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#
#     # 9C73F8
#
#     if "visibility" not in st.session_state:
#         st.session_state.visibility = "visible"
#         st.session_state.disabled = False
#
#
#
# items = []
#
#
# def page1(selected):
#     if selected == "Intro":
#         # Header
#         st.title("hh.ru analyzer")
#         st.subheader('*Система для автоматического анализа резюме кандидатов*')
#
#         st.divider()
#
#         with st.container():
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.header('Use Cases')
#                 st.markdown(
#                     """
#                     - _Remote work got you thinking about relocation?_
#                     - _Looking for a new vacation spot?_
#                     - _Conducting market research for product expansion?_
#                     - _Just here to play and learn?_
#                     """
#                 )
#             with col2:
#                 lottie2 = load_lottiefile("streamlit_bert/static/analyze_lottie.json")
#                 st_lottie(lottie2, key='place', height=300, width=300)
#
#         st.divider()
#
#
# def page2(selected):
#     # Search Page
#     if selected == "Inference":
#         st.header('Inference')
#         st.divider()
#
#         with st.container():
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader('Загрузите json с вакансией')
#                 default_code = '''{
#             "id": "95951496",
#             "name": "Менеджер по развитию территории г. Иркутск",
#             "area": "Иркутск",
#             "salary": {
#                 "start": 150000,
#                 "to": 250000,
#                 "currency": "RUR"
#             },
#             "published_at": "2024-04-02T08:16:44+0300",
#             "trusted_employer": true,
#             "employer_name": "Айкрафт"
#
#         }'''
#                 uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type=["json", "csv"])
#
#                 btn_settings_editor_btns = [{
#                     "name": "copy",
#                     "feather": "Copy",
#                     "hasText": True,
#                     "alwaysOn": True,
#                     "commands": ["copyAll"],
#                     "style": {"top": "0rem", "right": "0.4rem"}
#                 }]
#
#                 index = st.text_input("")
#
#
#
#                 if uploaded_file is not None:
#
#                     try:
#                         vacancy = pd.read_csv(uploaded_file).vaccancy
#                         vacancy_sub = vacancy.iloc[int(index)]
#                         a, b = find_nearest_neighbors(vacancy_sub)
#                         st.title(vacancy_sub[vacancy_sub.find(":") + 1:])
#
#                         vec = model.encode(data.iloc[1622])
#                         vec2 = model.encode(vacancy_sub)
#
#                         # util.cos_sim(embeddings[0] - means['mean_resume'].values,
#                         #              embeddings[1] - means['mean_vac'].values)
#
#                         sim = util.cos_sim(vec - means['mean_resume'].values, vec2 - means['mean_vac'].values)
#
#                         st.title((sim + 1) / 2)
#
#                         # json_content = uploaded_file.read()
#                         #
#                         # # Decode bytes to string assuming UTF-8 encoding
#                         # json_string = json_content.decode('utf-8')
#                         # response_dict = code_editor(json_string, lang="json", buttons=btn_settings_editor_btns,
#                         #                             height=15)
#
#                         # infer_model(data, model, means)
#
#
#                     except Exception as e:
#                         pass
#                         # st.warning(e, icon="⚠️")
#                 with col2:
#                     st.title(data.iloc[1].text)
#                     try:
#                         # with st.container(height=300):
#                         #     st.markdown("<br>".join(data), unsafe_allow_html=True)
#                         with st.container(height=646):
#                             for i in range(k):
#                                 text_sub, dist_sub = a[i]
#                                 st.text(text_sub.text)
#                                 st.text(round(1 - dist_sub, 2))
#                                 st.text(b[i])
#                                 st.divider()
#
#                                 # display_custom_item(item)
#                     except Exception as e:
#                         print(e)
#
#
# def page3(selected):
#     # Search Page
#     if selected == "About":
#         st.subheader('Select Location')
#
#
# def menu():
#
#     init()
#     # Options Menu
#     with st.sidebar:
#         selected = option_menu('Menu', ["Intro", 'Inference', 'About'],
#                                icons=['house', 'hexagon', 'info-circle'], menu_icon='intersect', default_index=0)
#     page1(selected)
#     page2(selected)
#     page3(selected)
#
#
# if __name__ == "__main__":
#     menu()
