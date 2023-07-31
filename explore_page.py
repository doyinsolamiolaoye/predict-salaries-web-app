import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_cat(categories, cutoff):
    categorical_map = {key:key if value > cutoff else "Other" for key, value in categories.items()}
    return categorical_map

def clean_year(x):
    if x == "Less than 1 year":
        return 0.5
    if x == "More than 50 years":
        return 50
    return float(x)

def clean_edu(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"

@st.cache_data
def load_data():
    df = pd.read_csv("stack-overflow-developer-survey-2020/survey_results_public.csv")
    df = df[["Country", "EdLevel","YearsCodePro","Employment","ConvertedComp"]]
    df.rename({"ConvertedComp":"Salary"}, axis=1, inplace=True)
    df = df[df["Salary"].notnull()]
    df.dropna(inplace=True)
    df = df[df["Employment"] == "Employed full-time"]
    df.drop("Employment", axis=1, inplace=True)
    country_map = shorten_cat(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[(df["Salary"] <= 250000) & (df["Salary"] >= 10000)]
    df = df[df["Country"] != "Other"]
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_year)
    df["EdLevel"] = df["EdLevel"].apply(clean_edu)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
        """
    )
    data = df.Country.value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)

    st.write(
        """
    ### Mean Salary based on Country
        """
    )
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    ### Mean Salary based on Years of Experience
        """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
