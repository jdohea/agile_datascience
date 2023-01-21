
from data_science.src.models.train_model import *
from pydantic import BaseModel
from fastapi import FastAPI
from spotlightRecommender import Recommender


app = FastAPI()
RecClass = Recommender()


class Message(BaseModel):
    movies = "Toy Story (1995),GoldenEye (1995)"
    number_of_movies = '2'
    genre = 'None'

class Retrain(BaseModel):
    number_of_iterations='50'

@app.get("/")
def hello():
    return 'The app is running'


@app.post("/get_movie")
def send_message(message: Message):
    movies = message.movies.split(',')
    number_of_movies = int(message.number_of_movies)
    if message.genre =='None':
        message.genre=None
    rec, bool =RecClass.get_prediction(movies,n_movies=number_of_movies, genre=message.genre)
    return str(rec[0])

@app.post("/get_movies")
def send_message(message: Message):
    movies = message.movies.split(',')
    number_of_movies = int(message.number_of_movies)
    if message.genre =='None':
        message.genre=None
    rec, bool =RecClass.get_prediction(movies,n_movies=number_of_movies, genre=message.genre)
    ans = ''
    for i in rec:
        ans += i+', '
    return ans

@app.post("/retrain_model")
def send_message(iterations: Retrain):
    RecClass.experiment(int(iterations.number_of_iterations))
    return 'New models retrained and best model is active'



if __name__=="__main__":
    train_and_evaluate()

# movie names to id's
# format of the input should be a list of ids ?

#test the basic parts of spotlight Recommender and deploy with container on google cloud
