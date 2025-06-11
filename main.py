import streamlit as st
import pandas as pd


PATH = "data/smart_manufacturing_data_cleaned.csv"


@st.cache_data
def read_data():
    df = pd.read_csv(PATH)
    return df


if __name__ == '__main__':
    df = read_data()
