import streamlit as st
import pandas as pd

PATH = "data/smart_manufacturing_data_cleaned.csv"


@st.cache_data
def read_data():
    df = pd.read_csv(PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    return df


@st.cache_data
def csv_convert(df):
    return df.to_csv(index=False).encode("utf-8")


st.title("Baixar Dados Operacionais")

df = read_data()

with st.expander("Selecionar colunas"):
    colunas = st.multiselect(
        "Escolha as colunas que deseja baixar:",
        list(df.columns),
        default=list(df.columns),
    )

filtered_df = df[colunas]

st.dataframe(filtered_df)
st.markdown(f":gray[{filtered_df.shape[0]} linhas × {filtered_df.shape[1]} colunas]")

st.download_button(
    label="Baixar CSV",
    data=csv_convert(filtered_df),
    file_name="dados_operacionais.csv",
    mime="text/csv",
)
