import streamlit as st
import pandas as pd
import joblib as jb

water_model = jb.load(r'#enter your path')
water_features = jb.load(r'#enter your path')

electricity_model = jb.load(r'#enter your path')
electricity_features = jb.load(r'#enter your path')

st.title("Utility Usage Prediction System")


prediction_type = st.selectbox(
    "Select what you want to predict:",
    ["Water Usage", "Electricity Usage"]
)
st.divider()

if prediction_type == "Water Usage":
    st.subheader("Water Usage Prediction")

    occ_01 = st.selectbox("Person 1 Present?", ["Occupied", "Not Occupied"])
    occ_02 = st.selectbox("Person 2 Present?", ["Occupied", "Not Occupied"])
    occ_03 = st.selectbox("Person 3 Present?", ["Occupied", "Not Occupied"])
    occ_04 = st.selectbox("Person 4 Present?", ["Occupied", "Not Occupied"])
    occ_05 = st.selectbox("Person 5 Present?", ["Occupied", "Not Occupied"])

    if st.button("Predict"):
        new_data = pd.DataFrame(0, index=[0], columns=water_features)

        new_data["occ_01"] = 1 if occ_01 == "Occupied" else 0
        new_data["occ_02"] = 1 if occ_02 == "Occupied" else 0
        new_data["occ_03"] = 1 if occ_03 == "Occupied" else 0
        new_data["occ_04"] = 1 if occ_04 == "Occupied" else 0
        new_data["occ_05"] = 1 if occ_05 == "Occupied" else 0

        prediction = water_model.predict(new_data)[0]

        st.success(f"Predicted Water Usage: {prediction:.2f} liters")

else:
    st.subheader("Electricity Usage Prediction")

    building = st.selectbox(
        "Select Building",
        sorted([col.replace("building_", "") 
                for col in electricity_features if col.startswith("building_")])
    )

    occupied = st.selectbox("Is the house occupied?", ["Yes", "No"])
    hour = st.slider("Hour of the day", 0, 23, 18)
    day_of_week = st.slider("Day of week (0=Mon, 6=Sun)", 0, 6, 3)

    if st.button("Predict"):
        new_data = pd.DataFrame(0, index=[0], columns=electricity_features)

        new_data["occupied"] = 1 if occupied == "Yes" else 0
        new_data["hour"] = hour
        new_data["day_of_week"] = day_of_week

        building_col = f"building_{building}"
        if building_col in new_data.columns:
            new_data[building_col] = 1

        prediction = electricity_model.predict(new_data)[0]

        st.success(f"Predicted Electricity Usage: {prediction:.2f} kWh")

