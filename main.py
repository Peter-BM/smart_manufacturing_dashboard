import streamlit as st
import pandas as pd
import plotly.express as px

PATH = "data/smart_manufacturing_data_cleaned.csv"


@st.cache_data
def read_data():
    df = pd.read_csv(PATH)
    create_date_feature(df)
    return df


def create_date_feature(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date


def format_quarter(quarter):
    quarters = {"Madrugada": 0, "Manhã": 1, "Tarde": 2, "Noite": 3}

    return quarters[quarter]


def display_machine_vibration_graph(df, query, selected_machine):
    filtered_df = df.query(query)

    if filtered_df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    fig = px.line(
        filtered_df,
        x="timestamp",
        y="vibration",
        title=f"Vibração da máquina {selected_machine}",
        labels={"vibration": "Vibração", "timestamp": "Data e Hora"},
    )
    st.plotly_chart(fig, use_container_width=True)


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

        with col1:
            start_date = st.slider(
                "Data inicial",
                min_value=min_date,
                max_value=max_date,
                value=min_date,
                format="DD/MM/YYYY",
            )
            start_quarter = st.selectbox("Periodo inicial", options=quarters, index=0)
            start_quarter = format_quarter(start_quarter)

        with col2:
            end_date = st.slider(
                "Data final",
                min_value=min_date,
                max_value=max_date,
                value=max_date,
                format="DD/MM/YYYY",
            )
            end_quarter = st.selectbox("Periodo final", options=quarters, index=2)
            end_quarter = format_quarter(end_quarter)

        selected_machine = st.selectbox("Máquina", options=df["machine"].unique())

        submitted = st.form_submit_button("Análisar", type="primary")

    filter = """
    (@start_date <= date and date <= @end_date) and \
    (@start_quarter <= slot_6h <= @end_quarter) and \
    (machine == @selected_machine)
    """

    display_machine_vibration_graph(df, filter, selected_machine)
