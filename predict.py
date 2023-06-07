import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()
regressor = data["model"]
le_age = data["le_age"]
le_age1 = data["le_age1"]
le_freq = data["le_freq"]
le_country = data["le_country"]
le_ed = data["le_ed"]
le_employ = data["le_employ"]
le_gender = data["le_gender"]
le_lww = data["le_lww"]
le_ld = data["le_ld"]
le_mt = data["le_mt"]
le_mtd = data["le_mtd"]
le_ug = data["le_ug"]


def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""###""")
    countries = ('Choose an Option', 'United States', 'United Kingdom', 'France', 'Brazil',
                 'Canada', 'Germany', 'Netherlands', 'India', 'Australia', 'Other')
    education = ('Choose an Option', 'Bachelor’s degree', 'Master’s degree', 'Less than a Bachelors',
                 'Post grad')
    employment = ('Choose an Option', 'Employed full-time',
                  'Independent contractor, freelancer, or self-employed',
                  'Employed part-time')
    freq = ('Choose an Option', 'Yearly', 'Monthly', 'Weekly')
    gender = ('Choose an Option', 'Man', 'Woman', 'Other')
    languages = ('Choose an Option', 'Python', 'HTML/CSS', 'C#', 'Bash/Shell/PowerShell', 'Assembly',
                 'Go', 'JavaScript', 'C', 'C++', 'Java', 'TypeScript', 'Dart',
                 'Scala', 'R', 'Objective-C', 'PHP', 'Kotlin', 'Haskell', 'Julia',
                 'SQL', 'Ruby', 'Swift', 'Rust')
    new_languages = ('Choose an Option', 'JavaScript', 'HTML/CSS', 'Go', 'C#', 'Bash/Shell/PowerShell',
                     'Python', 'Kotlin', 'Assembly', 'C', 'Dart', 'Haskell', 'Julia',
                     'C++', 'TypeScript', 'Java', 'Rust', 'Objective-C', 'Scala',
                     'Ruby', 'R', 'SQL', 'Swift', 'VBA', 'PHP', 'Perl')
    tech = ('Choose an Option', 'Ansible', 'Pandas', 'Node.js', '.NET', 'Keras', '.NET Core',
            'Hadoop', 'Apache Spark', 'Unity 3D', 'Cordova', 'Flutter',
            'Teraform', 'React Native', 'Chef', 'Unreal Engine', 'TensorFlow',
            'Puppet', 'Xamarin', 'Torch/PyTorch')
    new_tech = ('Choose an Option', 'Unity 3D', 'Pandas', 'Node.js', '.NET', '.NET Core', 'Keras',
                'Flutter', 'Ansible', 'Apache Spark', 'React Native', 'Cordova',
                'TensorFlow', 'Teraform', 'Chef', 'Hadoop', 'Unreal Engine',
                'Xamarin', 'Torch/PyTorch', 'Puppet')
    undergrad = ('Choose an Option', 'Computer science', 'Mathematics or statistics', 'Natural science',
                 'Information technology', 'Humanities', 'Social science',
                 'Web development', 'Another engineering discipline', 'No major',
                 'business', 'Health science', 'Fine arts')
    age = st.slider("Age", 0, 100, 1)
    age1 = st.slider("Age When Person Began Coding", 0, 100, 1)
    g = st.selectbox("Gender", gender)
    country = st.selectbox("Country", countries)
    f = st.selectbox("Frequency of Salary", freq)
    edu = st.selectbox("Education Level", education)
    ug = st.selectbox("Undergraduate Major", undergrad)
    em = st.selectbox("Employment Type", employment)
    lang = st.selectbox("Language Worked With", languages)
    lang1 = st.selectbox("Language Desired to Work With", new_languages)
    misc = st.selectbox("Technology Worked With", tech)
    misc1 = st.selectbox("Technology Desired to Work Work With", new_tech)
    st.write("""###""")
    ok = st.button("Calculate Salary")
    if ok:
        z = np.array(
            [[age, age1, f, country, edu, em, g, lang, lang1, misc, misc1, ug]])
        z[:, 0] = le_age.transform(z[:, 0])
        z[:, 1] = le_age1.transform(z[:, 1])
        z[:, 2] = le_freq.transform(z[:, 2])
        z[:, 3] = le_country.transform(z[:, 3])
        z[:, 4] = le_ed.transform(z[:, 4])
        z[:, 5] = le_employ.transform(z[:, 5])
        z[:, 6] = le_gender.transform(z[:, 6])
        z[:, 7] = le_lww.transform(z[:, 7])
        z[:, 8] = le_ld.transform(z[:, 8])
        z[:, 9] = le_mt.transform(z[:, 9])
        z[:, 10] = le_mtd.transform(z[:, 10])
        z[:, 11] = le_ug.transform(z[:, 11])
        z = z.astype(int)
        salary = regressor.predict(z)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
