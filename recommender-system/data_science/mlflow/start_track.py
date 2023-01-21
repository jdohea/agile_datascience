import mlflow
from pathlib import Path

# create experiments dir
MODEL_REGISTRY = Path("experiments")
Path(MODEL_REGISTRY).mkdir(exist_ok=True)  
# Set tracking URI
mlflow.set_tracking_uri("file://" + str(MODEL_REGISTRY.absolute()))
# Set experiment
mlflow.set_experiment(experiment_name="baselines")
