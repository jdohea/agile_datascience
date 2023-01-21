# General libraries
import numpy as np
import mlflow
import torch

# Spotlight specific tools
import spotlight.cross_validation #import user_based_train_test_split
############################################################
# Goal: remove the need for synthetic data
#from spotlight.datasets.synthetic import generate_sequential
# Actual data set
from spotlight.datasets.movielens import get_movielens_dataset
############################################################
from spotlight.evaluation import sequence_mrr_score
from spotlight.sequence.implicit import ImplicitSequenceModel

def train_and_evaluate(n_iter=1, representation='cnn', loss='bpr'):

    mlflow.set_tracking_uri("http://127.0.0.1:5000/")
    mlflow.set_experiment('Movielens experiment')

    movielens = get_movielens_dataset()
    train, test = spotlight.cross_validation.user_based_train_test_split(movielens)
    train = train.to_sequence()
    test = test.to_sequence()

    with mlflow.start_run() as mlops_run:
        model = ImplicitSequenceModel(n_iter=n_iter, representation=representation, loss=loss)
        model.fit(train, verbose=True)
        test_mrr_score = np.mean(sequence_mrr_score(model, test))

        mlflow.log_param("n_iter", n_iter)
        mlflow.log_param("representation", representation)
        mlflow.log_param("loss", loss)
        mlflow.log_metric("test_mrr_score", test_mrr_score)

        run = mlflow.active_run().info.run_id
        torch.save(model, 'data_science/src/models/model_' + str(run))
    return 'new model created'
 
if __name__=="__main__":
    train_and_evaluate()