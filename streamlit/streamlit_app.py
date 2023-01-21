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

######## CONSTANTS
num_docs = 10
num_docs2 = 5
col_name = 'algebros'
col_name2 = 'streamlit_input'
text = '''---'''

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

def retrieve_movies():
    conn = init_connection()
    database = get_database(conn)
    col = database.movie_names
    display = get_genre_movies(col, ss.dbgenre, num_docs = num_docs)
    ss.txt = ''
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


# st.write(""" # 🎥Movie🎬Recommender™️ Algebros🍆INC. v4.20 🗿 """)
st.write("""
    # Movie Recommender Algebros INC.""")
st.write("""
    ##### Choose the movies you have watched and enjoyed from the following ones
""")

st.markdown(text)



actual_email = "email"
actual_password = "password"

with st.sidebar:
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials for your custom recommendations!")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
        placeholder.empty()
        st.success("Login successful")
    elif submit and email != actual_email and password != actual_password:
        st.error("Login failed")
    else:
        pass

    placeholder2 = st.empty()
    with placeholder2.form("sign"):
        st.markdown("""#### No account yet? Sign up to save your recommendations!""")
        email2 = st.text_input("Email ")
        password2 = st.text_input("Password ", type="password")
        repeat = st.text_input("Repeat Password  ", type="password")
        submit2 = st.form_submit_button("Sign up")


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
    leftr, centerr, rightr = st.columns([2,1,1])
    with leftr: 
        number = st.slider("How many recommendations do you want?", 1,5)
    with rightr: 
        ss.submit = st.button('  🎥 Recommend me!')

if ss.submit:
    ss.txt = ss.txt[:len(ss.txt)-1]
    data = {"movies":ss.txt,"number_of_movies": number ,"genre": ss.dbgenre }
    response = requests.post("http://108.142.183.229:8080/get_movies",json=data)
    #st.write(f''' We are sending the recommender the following movie(s): {ss.txt}''')
    st.write(f''' Our recommender suggests the following movie(s): 
        {response.text}
    ''')

# "beta", st.session_state