import pandas as pd
import numpy as np
import joblib as jb

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('water.csv')

occ_cols = ["occ_01", "occ_02", "occ_03", "occ_04", "occ_05"]
for col in occ_cols:
    df[col] = df[col].map({
        "Occupied": 1,
        "Not Occupied": 0
    })


X = df[occ_cols]
y = df["water_use_l"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

model = RandomForestRegressor(n_estimators = 200, random_state = 42)
model.fit(X_train, y_train)

jb.dump(model, "water_model.pkl")
jb.dump(X.columns.tolist(), "water_features.pkl")

print("Model Saved.")