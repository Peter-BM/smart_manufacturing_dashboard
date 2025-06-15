import streamlit as st
import pandas as pd
import plotly.express as px

PATH = "data/smart_manufacturing_data_cleaned.csv"


@st.cache_data
def read_data():
    df = pd.read_csv(PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    return df


def display_machine_comparison_chart(df, features, machines, agg):
    col1, col2 = st.columns(2)

    filtered_df = df[df["machine"].isin(machines)]

    for i, feature in enumerate(features):
        feature_label = feature.replace("_", " ").capitalize()

        grouped = (
            filtered_df.groupby("machine")[feature]
            .agg("mean" if agg == "mean" else "max")
            .reset_index()
        )

        title = f"{'Média' if agg == 'mean' else 'Máximo'} de {feature_label.lower()} por máquina"

        fig = px.bar(
            grouped,
            x="machine",
            y=feature,
            labels={"machine": "Máquina", feature: feature_label},
            title=title,
        )

        (col1 if i % 2 == 0 else col2).plotly_chart(fig, use_container_width=True)


st.title("Comparativo Personalizado entre Máquinas")

df = read_data()

all_features = [
    "vibration",
    "temperature",
    "energy_consumption",
    "pressure",
    "humidity",
    "predicted_remaining_life",
]
all_machines = df["machine"].unique().tolist()

selected_features = st.multiselect(
    "Selecione as métricas:", options=all_features, default=["vibration"]
)
selected_machines = st.multiselect(
    "Selecione as máquinas:", options=all_machines, default=all_machines[0:2]
)
agg_method = st.radio(
    "Tipo de agregação:",
    options=["mean", "max"],
    format_func=lambda x: "Média" if x == "mean" else "Máximo",
)

if selected_features and selected_machines:
    display_machine_comparison_chart(
        df, selected_features, selected_machines, agg_method
    )
else:
    st.info("Selecione pelo menos uma métrica e uma máquina.")
