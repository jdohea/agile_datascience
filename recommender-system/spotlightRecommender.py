import numpy as np 
import pandas as pd
import commands
import mlflow
from torch import save
from torch import load
from numpy.random import permutation
import time

# Spotlight specific tools
from spotlight.sequence.implicit import ImplicitSequenceModel # model to be constructed
from spotlight.evaluation import sequence_mrr_score # Evaluate model
from spotlight.interactions import Interactions # Generate dataset format needed for Spotlight
from spotlight.cross_validation import user_based_train_test_split # Split data

class Recommender():
    
    def __init__(self) -> None:
        self.most_recent_run = None
        self.active_model = None
        self.experiment(number_of_iterations=1)


    def get_database(self):
        '''
        This function will pull the movielens 100K dataset as an interaction
        database object and convert it to a useable sequence.

        Input: NONE
        Output: pymongo Database object
        '''
        # get data to be trained on
        ####################################################
        # NEXT STEP: Add in additional data from prior recommedations!
        conn = commands.connect()
        data = commands.get_data(conn, col_name='movie_data')
        ####################################################
        return Interactions(user_ids = data['user_id'].values.astype(np.int32), item_ids = data['item_id'].values.astype(np.int32),
                            ratings = data['rating'].values.astype(np.float32), timestamps = data['timestamp'].values.astype(np.int32))


    def train_model(trainingSet, n):
        '''
        This function trains an Implicit Sequential model on the given
        sequential data set.

        Input: Sequential training set, number of training epochs
        Output: Sequential model
        '''
        trainingSet = trainingSet.to_sequence()

        # Construct model on training
        SequentialRecommender = ImplicitSequenceModel(n_iter=n,
                                    representation='cnn',
                                    loss='bpr')

        SequentialRecommender.fit(trainingSet)
        return SequentialRecommender

    def get_prediction(self, movieSequence, n_movies = 1, genre=None):
        '''
        This function intakes a sequence of movie ids from our data base
        and returns a score for every other movie that represents the likelihood
        the given sequence would produce that movie.

        Addition: Added functionality to perform permutations on the sequences to
        differing predictions
        Extra addition: Added functionality to only output movies from the
        specified genre. By default not filtering by genre

        ###Input: list-like (sequence of movie id), integer (number of desired movie suggestions), string (desired genre of movie suggestions)
        ###Output: list of integers (movie id list), boolean (if predictions stopped early)
        '''
        SequentialRecommender = self.active_model
        conn = commands.connect()
        db = commands.get_database(conn)
        col = commands.get_collection(db, col_name='movie_names')

        accepted_genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                        'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
                        'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                        'Thriller', 'War']

        if genre != None:
            if genre in accepted_genres:
                genre_movies = commands.get_movies_by_genre(col, genre)
                genre_movies = list(map(int, genre_movies))
            else:
                genre = None
        
        Candidates = commands.get_movie_ids(col, movieSequence)
        init_len = len(Candidates)
        movieSequence = list(map(int, Candidates))
        StoppingCheck = n_movies ** 2
        i = 0
        while len(Candidates) < n_movies + init_len:
            LikelihoodScore = SequentialRecommender.predict(permutation(movieSequence))
            BestOption = np.argmax(LikelihoodScore) + 1 # shifting is needed as movie id starts at 1 not 0
            i += 1
            top_index = 0

            if i > StoppingCheck:
                Candidates = commands.get_movie_names(col, Candidates[init_len:])
                return Candidates, True

            validOption = True

            while str(BestOption) in Candidates or (genre != None and BestOption not in genre_movies):
                top_index += 1
                LikelihoodScore[BestOption-1] = 0
                BestOption = np.argmax(LikelihoodScore) + 1

                if top_index > 10:
                    validOption = False
                    break

            if not validOption: continue
                
            Candidates.append(str(BestOption))
        
        Candidates = commands.get_movie_names(col, Candidates[init_len:])
        return Candidates, False

    def train_and_evaluate(self, trainingSet, validationSet, ns=[1,2]):
            '''
            This function trains an Implicit Sequential model on the given
            sequential data set and uploads its information to MLFlow

            Input: Sequential training and validation sets, number of training epochs
            '''
            mlflow.set_tracking_uri("http://127.0.0.1:5000/")
            id = 'Movielens_experiment_'+str(time.time())
            experiment_id = mlflow.create_experiment(
                id
            )
            trainingSet = trainingSet.to_sequence()
            validationSet = validationSet.to_sequence()
            experiment = mlflow.set_experiment(experiment_id=experiment_id)
            self.most_recent_experiment = experiment.experiment_id
            for n in ns:
                with mlflow.start_run(experiment_id=experiment.experiment_id) as mlops_run:
                    # Construct model on training
                    SequentialRecommender = ImplicitSequenceModel(n_iter=n,
                                                representation='cnn',
                                                loss='bpr')

                    SequentialRecommender.fit(trainingSet)

                    val_mrr_score = np.mean(sequence_mrr_score(SequentialRecommender, validationSet))

                    mlflow.log_param("n_iter", n)
                    mlflow.log_param("representation", 'cnn')
                    mlflow.log_param("loss", 'bpr')
                    mlflow.log_metric("val_mrr_score", val_mrr_score)
                    run = mlflow.active_run().info.run_id
                    model_name = 'data_science/src/models/' + str(run)
                    mlflow.log_param('model_name',model_name)
                    save(SequentialRecommender, model_name)
                    self.most_recent_run = model_name
                mlflow.end_run()


    def get_train_val(self):
            data = self.get_database()
            train,val = user_based_train_test_split(data,test_percentage=0.2)
            return train,val
    
    def load_model(self):
        return load(self.most_recent_run)
    
    def experiment(self, number_of_iterations):
        train, eval = self.get_train_val()
        self.train_and_evaluate(train, eval,ns=[number_of_iterations])
        self.active_model = self.load_model()


if __name__=="__main__":
    movieSet = Recommender().get_database()
    Recommender().train_and_evaluate(movieSet, 50)
    print('New model created')
    
        

