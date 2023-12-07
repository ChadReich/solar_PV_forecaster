import numpy as np
import pandas as pd
from sklearn.linear_model import LassoLarsCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('solar_PV_forecaster/solar_project_data.csv', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('ptot', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['ptot'], random_state=None)

# Average CV score on the training set was: -2.143490963820017e-26
exported_pipeline = make_pipeline(
    RobustScaler(),
    LassoLarsCV(normalize=False)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
