# run this once 
# if ss.init:
#     conn = init_connection()
#     database = get_database(conn)
#     col = database.movie_names
#     rows = get_rows_col(col,num_docs = num_docs)
#     display = [i["name"] for i in rows]
#     ss.display_checkbox = {}
#     for i in range (num_docs):
#         ss.display_checkbox["checkbox_{0}".format(i)] = st.checkbox(f"{display[i]}")
#     ss.init = False
#     ss.displayc = True
# else: 
#     for i in range (num_docs):
#         ss.display_checkbox["checkbox_{0}".format(i)] = st.checkbox(f"{display[i]}")

# rows = get_rows(conn)

# ss.display_checkbox = {}
# for i in range (num_docs):
#     ss.display_checkbox["checkbox_{0}".format(i)] = st.checkbox(f"{display[i]}")

# ss.checkbox_0 = st.checkbox(f"{display[0]}")
# ss.checkbox_1 = st.checkbox(f"{display[1]}")
# ss.checkbox_2 = st.checkbox(f"{display[2]}")
# ss.checkbox_3 = st.checkbox(f"{display[3]}")
# ss.checkbox_4 = st.checkbox(f"{display[4]}")
# ss.checkbox_5 = st.checkbox(f"{display[5]}")
# ss.checkbox_6 = st.checkbox(f"{display[6]}")
# ss.checkbox_7 = st.checkbox(f"{display[7]}")
# ss.checkbox_8 = st.checkbox(f"{display[8]}")
# ss.checkbox_9 = st.checkbox(f"{display[9]}")


# st.selectbox('Pick one', ['cats', 'dogs'])

# multiselect = st.multiselect('Buy', ['milk', 'apples', 'potatoes'])


### for agree array if agree send to recommender within recommend button

# st.write(f"""
#     
# """)

# for i in range(1,4):
#     st.write(f"""
#         insert.movie({i})
#     """)
#     col1, col2, col3, col4, col5 = st.columns([0.5,0.5,0.5,0.5,0.5])
#     with col1:
#         st.button('1', key=str(i)+'1')
#     with col2:
#         st.button('2', key=str(i)+'2')
#     with col3:
#         st.button('3', key=str(i)+'3')
#     with col4:
#         st.button('4', key=str(i)+'4')
#     with col5:
#         st.button('5', key=str(i)+'5')

# import requests
# 
# if __name__=='__main__':
#     data= {
#     "text": "movie_id1,movieid_2,movie_id3",
#     }
#     response = requests.post("http://104.47.164.128:8080/get_movie",json=data)
#     print(response.text)

thistuple = ("apple", "banana", "cherry")
print(thistuple[0])



# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
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


st.write(f'''
    <a target="_self" href="https://recommender.streamlit.app/">
        <button>
            Check out our Recommender 2.0!
        </button>
    </a>
    ''',
    unsafe_allow_html=True
)

"(beta) session state: " , st.session_state
