import streamlit as st
import pickle
import numpy as np


def load_model():
    with open("saved_steps.pkl", "rb") as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor_loaded = data["model"]
le_country_load = data['le_country']
le_edu_load = data["le_education"]
countries = le_country_load.classes_
education = le_edu_load.classes_

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    #st.write("{}".format())

    country = st.selectbox("Country", countries)
    education_level = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    okay = st.button("Calculate Salary")

    if okay:
        X = np.array([[country, education_level, experience]])
        X[:,0] = le_country_load.transform(X[:,0])
        X[:,1] = le_edu_load.transform(X[:,1])
        X = X.astype(float)

        salary = regressor_loaded.predict(X)
        st.subheader(f"The estimated salary is $ {salary[0]:,.2f}")
