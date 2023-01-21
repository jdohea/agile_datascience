import pymongo
import pandas as pd
import streamlit as st
# Initialize connection.
# Uses st.experimental_singleton to only run once.
#@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient("mongodb+srv://{}:{}@{}".format(st.secrets["mongo"]["username"],st.secrets["mongo"]["password"],st.secrets["mongo"]["host"]))

def get_database(conn):
    return conn.algebros

def get_collection(db, col_name='streamlit_input'):
    if col_name == 'streamlit_input':
        return db.streamlit_input
    else:
        return db.algebros_collection


def insert_data(conn, data, col_name='streamlit_input'):
    database = get_database(conn)
    collection = get_collection(database, col_name)
    if col_name == 'streamlit_input':
        collection.insert_one(data)
    else:
        collection.deleteMany({})
        collection.insert_many(data)

def cursorToDF(cursor):
    return pd.DataFrame(cursor)

def get_data(conn, col_name='streamlit_input'):
    database = get_database(conn)
    collection = get_collection(database, col_name)
    response =  pd.DataFrame(collection.find())
    return cursorToDF(response)

def get_rows(conn, num_docs=5, col_name='streamlit_input'):
    results = []
    database = get_database(conn)
    collection = get_collection(database, col_name)
    cursor = collection.aggregate([ { '$sample': { 'size': num_docs } } ])
    for row in cursor:
        results.append(row)
    return results

def get_rows_col(collection, num_docs=5, col_name='streamlit_input'):
    results = []
    cursor = collection.aggregate([ { '$sample': { 'size': num_docs } } ])
    for row in cursor:
        results.append(row)
    return results

def display(num_docs = 5):

    return 

def get_movie_names(col, ids):
    
    data = col.find({"id": {"$in": ids}})
    names = [document["name"] for document in data]
    return names

def get_movie_ids(col, names):
    
    data = col.find({"name": {"$in": names}})
    ids = [document["id"] for document in data]
    return ids

def get_genre_movies(col, genre, num_docs=10):
    results = []
    if genre == 'None':
        return [i["name"] for i in get_rows_col(col, num_docs=num_docs)]
    else:
        cursor = col.aggregate([ 
            { "$match": { "{}".format(genre): { "$eq": '1' } } },
            { '$sample': { 'size': num_docs } } ])
        for row in cursor:
            results.append(row)
        return [i["name"] for i in results]