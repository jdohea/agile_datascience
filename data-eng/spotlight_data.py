from spotlight.datasets.movielens import get_movielens_dataset
import commands
import os

def get_dataset():
    return get_movielens_dataset(variant='1M')

def extract_spotlight():
    dataset = get_dataset()

    list_mongo = [] 
    users = dataset.user_ids
    items = dataset.item_ids
    ratings = dataset.ratings
    timestamps = dataset.timestamps

    for record in range(len(users)):
        dic = dict()
        dic['user_id'] = str(users[record])
        dic['item_id'] = str(items[record])
        dic['rating'] = str(ratings[record])
        dic['timestamp'] = str(timestamps[record])
        list_mongo.append(dic)

    return list_mongo

def get_movies(file_name):
    curr = os.path.curdir
    file_path = os.path.join(curr, file_name)

    with open(file_path, 'r', encoding = "ISO-8859-1") as f:
        df = f.readlines()
        f.close()
    return df

def format_movies(file_name):
    data = get_movies(file_name)
    lis = []

    for i in data:
        d = dict()
        a = i.split(sep=',')

        d['id'] = a[0]
        d['name'] = a[1]
        d['Action'] = a[2]
        d['Adventure'] = a[3]
        d['Animation'] = a[4]
        d['Children'] = a[5]
        d['Comedy'] = a[6]
        d['Crime'] = a[7]
        d['Documentary'] = a[8]
        d['Drama'] = a[9]
        d['Fantasy'] = a[10]
        d['Film-Noir'] = a[11]
        d['Horror'] = a[12]
        d['Musical'] = a[13]
        d['Mystery'] = a[14]
        d['Romance'] = a[15]
        d['Sci-Fi'] = a[16]
        d['Thriller'] = a[17]
        d['War'] = a[18]
        d['Western'] = a[19]


        lis.append(d)
    return lis
    
def extract_load(data_set = 'ratings', file_name='movies.txt'):
    conn = commands.connect()
    db = commands.get_database(conn)
    if data_set == 'ratings':
        col = commands.get_collection(db)
        data = extract_spotlight()
    else:
        col = commands.get_collection(db, col_name='movie_names')
        data = format_movies(file_name)
    commands.insert_data(col, data, col_name='other')


if __name__ == '__main__':
    extract_load(data_set = 'ratings')
    extract_load(data_set = 'movie_names')
