import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import pycaret
from pycaret.regression import *
import os

file = os.path.join(os.path.dirname(__file__), 'insurance.csv')
df = pd.read_csv(file)
train, test = train_test_split(df, test_size=0.2, random_state=42)
reg = setup(data=train, target='charges', train_size=0.7)
compare_models(sort='R2')

gbr = create_model('gbr')
tuned_gbr = tune_model(gbr)
plot_model(tuned_gbr, plot='error')
plot_model(tuned_gbr, plot='residuals')
plot_model(tuned_gbr, plot='feature')

predict_model(tuned_gbr, data=test)
gbr_final = finalize_model(tuned_gbr)
file = os.path.join(os.path.dirname(__file__), 'gbr_final')
save_model(gbr_final, file)
