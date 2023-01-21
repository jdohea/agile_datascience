import streamlit as st
import pandas as pd
from commands import get_database, init_connection, get_genre_movies
from streamlit import session_state as ss
import requests

#st.write("hi")
page_bg_img = '''
<style>
.stApp {
background-image: url("https://i.imgur.com/xpdLYGy.png");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# st.write(""" # 🎥Movie🎬Recommender™️ Algebros🍆INC. v4.20 🗿 """)
st.write("""
    # Movie Recommender Algebros INC.""")
st.write("""
    ##### Choose the movies you have watched and enjoyed from the following ones
""")

######## CONSTANTS
num_docs = 10
num_docs2 = 5
col_name = 'algebros'
col_name2 = 'streamlit_input'
text = '''---'''
st.markdown(text)
# @st.experimental_singleton
# def initdb():
#     ss.database = False
#     return ss.database
# 
# ss.database = initdb()
######## CONSTANTS

if 'database' not in st.session_state:
    st.session_state.database = False

if 'connect_button_text' not in st.session_state:
    ss.connect_button_text = 'Give me some movies!'

if 'submit' not in st.session_state:
    ss.submit = False

if 'dbgenre' not in st.session_state:
    ss.dbgenre = 'None'

if 'txt' not in ss:
    ss.txt = ''

if 'retrieve' not in ss:
    ss.retrieve = False

if 'display' not in ss:
    ss.display = {}


with st.sidebar:
    st.write("hi testing")

def retrieve_movies():
    conn = init_connection()
    database = get_database(conn)
    col = database.movie_names
    display = get_genre_movies(col, ss.dbgenre, num_docs = num_docs)
    return display
def retrieve_bool():
    ss.retrieve = True
    ss.txt = ''

def disp(display_list):
    left, right = st.columns(2)
    with left: 
        for i in range (0, num_docs2):
            display_checkbox["checkbox_{0}".format(i)] = st.checkbox(f"{display_list[i]}", key=i)
            if display_checkbox["checkbox_{0}".format(i)]:
                ss.txt = ss.txt + str(display_list[i]) + ','
    with right:
        for i in range (num_docs2 ,num_docs):
            display_checkbox["checkbox_{0}".format(i)] = st.checkbox(f"{display_list[i]}", key=i)
            if display_checkbox["checkbox_{0}".format(i)]:
                ss.txt = ss.txt + str(display_list[i]) + ','


ss.connect = st.button(ss.connect_button_text)
if ss.connect:
    st.snow()
    ss.d = retrieve_movies()
    ss.database = True

if ss.database:
    ss.connect_button_text = 'Show me new movies!'       
    display_checkbox = {}
    all_genres = ['None', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War']
    ss.dbgenre = st.selectbox('Filter by genre: ', all_genres, on_change=retrieve_bool)
    if ss.retrieve:
        ss.d = retrieve_movies()
    disp(ss.d)
    ss.retrieve = False
    st.markdown(text)
    ss.submit = st.button('Recommend me!')

if ss.submit:
    #for i in range(num_docs):
    #    if display_checkbox["checkbox_{0}".format(i)]:
    #        ss.txt = ss.txt + str(display[i]) + ','
    ss.txt = ss.txt[:len(ss.txt)-1]
    data = {"movies":ss.txt,"number_of_movies": "3","genre": ss.dbgenre }
    response = requests.post("http://108.142.183.229:8080/get_movies",json=data)
    st.write(f''' We are sending the recommender the following movie(s): {ss.txt}''')
    st.write(f''' Our recommender suggests the following movie: 
        {response.text}
    ''')

# "beta", st.session_state