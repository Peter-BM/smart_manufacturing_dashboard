import streamlit as st
import pandas as pd

PATH = "data/smart_manufacturing_data_cleaned.csv"


@st.cache_data
def read_data():
    df = pd.read_csv(PATH)
    create_date_feature(df)
    return df


def create_date_feature(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date


if __name__ == "__main__":
    df = read_data()

    st.title("Dados operacionais de maquinas industriais")

    with st.expander("Exibir tabela de dados"):
        st.dataframe(df)

    with st.form("data_form"):
        st.markdown("#### Filtros")

        col1, col2 = st.columns(2)

        min_date = df["date"].min()
        max_date = df["date"].max()
        quarters = ["Madrugada", "Manhã", "Tarde", "Noite"]

        selected_machine = st.selectbox(
            "Escolha uma máquina", options=df["machine"].unique()
        )

        with col1:
            start_date = st.slider(
                "Data inicial",
                min_value=min_date,
                max_value=max_date,
                value=min_date,
                format="DD/MM/YYYY",
            )
            start_quarter = st.selectbox("Periodo inicial", options=quarters, index=0)

        with col2:
            end_date = st.slider(
                "Data final",
                min_value=min_date,
                max_value=max_date,
                value=max_date,
                format="DD/MM/YYYY",
            )
            end_quarter = st.selectbox("Periodo final", options=quarters, index=2)

        submitted = st.form_submit_button("Análisar", type="primary")
