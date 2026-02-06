import streamlit as st
import pandas as pd
import joblib as jb
import matplotlib.pyplot as plt
import seaborn as sns


water_model = jb.load(r"#enter your path here")
water_features = jb.load(r"#enter your path here")

electricity_model = jb.load(r"#enter your path here")
electricity_features = jb.load(r"#enter your path here")

st.set_page_config(page_title="Utility Usage Prediction", layout="centered")
st.title("Sustainable Utility Usage Prediction System")


prediction_type = st.selectbox(
    "What do you want to predict?",
    ["Water Usage", "Electricity Usage"]
)

st.divider()


if prediction_type == "Water Usage":
    st.subheader("🚿 Water Usage Prediction")

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

        
        typical_water = 500  # liters (reasonable reference value)

        st.success(f"Predicted Water Usage: **{prediction:.2f} liters**")

        
        fig, ax = plt.subplots()
        sns.barplot(
            x=["Typical Usage", "Your Predicted Usage"],
            y=[typical_water, prediction],
            ax=ax
        )
        ax.set_ylabel("Liters")
        ax.set_title("Water Usage Comparison")

        st.pyplot(fig)

        if prediction > typical_water:
            st.warning("Your water usage is higher than typical households.")
        else:
            st.success("Your water usage is within normal limits.")


else:
    st.subheader("⚡ Electricity Usage Prediction")

    building_list = sorted(
        [col.replace("building_", "")
         for col in electricity_features if col.startswith("building_")]
    )

    building = st.selectbox("Select Building", building_list)
    occupied = st.selectbox("Is the house occupied?", ["Yes", "No"])
    hour = st.slider("Hour of the Day", 0, 23, 18)
    day_of_week = st.slider("Day of Week (0 = Mon, 6 = Sun)", 0, 6, 3)

    if st.button("Predict"):
        new_data = pd.DataFrame(0, index=[0], columns=electricity_features)

        new_data["occupied"] = 1 if occupied == "Yes" else 0
        new_data["hour"] = hour
        new_data["day_of_week"] = day_of_week

        building_col = f"building_{building}"
        if building_col in new_data.columns:
            new_data[building_col] = 1

        prediction = electricity_model.predict(new_data)[0]

        
        typical_electricity = 1.2 

        st.success(f"⚡ Predicted Electricity Usage: **{prediction:.2f} kWh**")

        
        fig, ax = plt.subplots()
        sns.barplot(
            x=["Typical Usage", "Your Predicted Usage"],
            y=[typical_electricity, prediction],
            ax=ax
        )
        ax.set_ylabel("kWh")
        ax.set_title("Electricity Usage Comparison")

        st.pyplot(fig)

        if prediction > typical_electricity:
            st.warning("Your electricity usage is higher than typical households.")
        else:
            st.success("Your electricity usage is within normal limits.")


st.divider()
st.caption(
    "This system predicts expected household water and electricity usage "
    "to promote responsible consumption and sustainability.")
