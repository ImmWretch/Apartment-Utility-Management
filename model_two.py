import pandas as pd
import numpy as np
import joblib as jb

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('electricity.csv')

df["occupied"] = df["occupied"].astype(int)

X = df.drop(columns=["electrcity_use_kwh"])
y = df["electrcity_use_kwh"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

model = RandomForestRegressor(n_estimators = 200, random_state = 42)
model.fit(X_train, y_train)

jb.dump(model, "electricity_model.pkl")
jb.dump(X.columns.tolist(), "electric_features.pkl")
print("Model Saved.")