import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


def clean_gender(x):
    if x == 'Man':
        return 'Man'
    if x == 'Woman':
        return 'Woman'
    return 'Other'


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_undergradmajor(x):
    if 'Computer science' in x:
        return 'Computer science'
    if 'natural science' in x:
        return 'Natural science'
    if 'information technology' in x:
        return 'Information technology'
    if 'humanities' in x:
        return 'Humanities'
    if 'social science' in x:
        return "Social science"
    if 'Web development' in x:
        return 'Web development'
    if 'Another engineering discipline' in x:
        return 'Another engineering discipline'
    if 'never' in x:
        return "No major"
    if 'business' in x:
        return "business"
    if 'health science' in x:
        return "Health science"
    if 'Fine arts' in x:
        return "Fine arts"
    return x


def clean_language_worked_with(i):
    if ";" in i:
        k = i.index(";")
        j = i[:k]
        return j
    else:
        return i


def desired_language(i):
    if ";" in i:
        k = i.index(";")
        j = i[:k]
        return j
    else:
        return i


def misc_clean(i):
    if ";" in i:
        k = i.index(";")
        j = i[:k]
        return j
    else:
        return i


def desired_misc_clean(i):
    if ";" in i:
        k = i.index(";")
        j = i[:k]
        return j
    else:
        return i


@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    relevant_columns = ['Age', 'Age1stCode', 'CompFreq', 'ConvertedComp',
                        'Country', 'EdLevel', 'Employment', 'Gender',
                        'LanguageWorkedWith', 'LanguageDesireNextYear', 'MiscTechWorkedWith',
                        'MiscTechDesireNextYear', 'UndergradMajor', 'YearsCode']
    df = df[relevant_columns]
    df = df.dropna()
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df['Gender'] = df['Gender'].apply(clean_gender)
    df['YearsCode'] = df['YearsCode'].apply(clean_experience)
    df["UndergradMajor"] = df["UndergradMajor"].apply(clean_undergradmajor)
    df["LanguageWorkedWith"] = df["LanguageWorkedWith"].apply(
        clean_language_worked_with)
    df["LanguageDesireNextYear"] = df["LanguageDesireNextYear"].apply(
        desired_language)
    df["MiscTechWorkedWith"] = df["MiscTechWorkedWith"].apply(misc_clean)
    df["MiscTechDesireNextYear"] = df["MiscTechDesireNextYear"].apply(
        desired_misc_clean)
    return df


df = load_data()


def show_explore_page():
    st.title("Explore Software Developer Salaries.")
    st.write(""" ### Stack Overflow Developer Survey 2020""")
    data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%",
            shadow=True, startangle=90)
    ax1.axis("equal")
    st.write("""### Data from different countries""")
    st.pyplot(fig1)
    st.write(""" ### Mean Salary Based On Education""")
    data = df.groupby(["EdLevel"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    st.write(""" ### Mean Salary Based On Experience""")
    data = df.groupby(["YearsCode"])[
        "Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
