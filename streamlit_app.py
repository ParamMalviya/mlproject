import streamlit as st
import requests

st.title("Student Performance Predictor")
st.write("Enter student details to predict math score")

gender = st.selectbox("gender", ["male", "female"])
race_ethnicity = st.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
parental_level_of_education = st.selectbox(
    "Parental Level of Education",
    ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"]
)
lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
test_preparation_course = st.selectbox("Test Preparation Course", ["none", "completed"])
reading_score = st.number_input("Reading Score", min_value=0, max_value=100, value=70)
writing_score = st.number_input("Writing Score", min_value=0, max_value=100, value=70)

if st.button("Predict math score"):
    payload = {
        "gender": gender,
        "race_ethnicity": race_ethnicity,
        "parental_level_of_education": parental_level_of_education,
        "lunch": lunch,
        "test_preparation_course": test_preparation_course,
        "reading_score": reading_score,
        "writing_score": writing_score
    }

    response = requests.post("http://localhost:8000/predict", json = payload)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Math Score: {result['Predicted_math_score']:.2f}")
    else:
        st.error("Prediction failed. Check backend logs.")