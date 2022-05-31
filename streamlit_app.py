import math
from collections import namedtuple

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Predictor de salarios.",
    page_icon="💸",
)

"""
# Predictor de sueldos en TI

Hola, aquí podrás obtener una predicción del sueldo bruto mensual en pesos argentinos que 
ganarías según el valor de las XXX variables de entrada que puedes ingresar en el panel de
la izquierda.

Los modelos regresores se realizaron tomando como base los datos de la encuesta de sueldos
llevada a cabo por la comunidad de sysarmy en el segundo semestre del 2021.

Para obtener más detalles del modelo implementado puedes entrar [aquí](https://www.jaimehmol.me).

@jaimehmol
"""

with st.form("Model prediction parameters"):
    ModelType = st.radio(
        "Choose your model",
        ["Linear Regression", "Random Forest"],
        help="At present, you can choose between 2 models (Linear Regression or \
        Random Forest) to predict the salary.",
    )
    predict = st.form_submit_button("Predecir")
    if predict:
        st.write("Tu sueldo debería ser:", 100000, "pesos argentinos", input_edad)


# c1, c2 = st.columns([2, 3])

with st.sidebar:
    input_edad = st.slider("Edad", 1, 80, 10)
    input_experiencia_anios = st.slider("Experiencia en años", 1, 80, 10)
    input_empresa_actual_anios = st.slider("Tiempo en empresa actual en años", 1, 80, 10)
    input_personas_a_cargo = st.slider("Personas a cargo", 1, 80, 10)
    input_sueldo_ajuste_total_2021 = st.slider("Ajuste de sueldo total en 2021", 1, 80, 10)
    input_recomendacion_laboral = st.slider("Nivel de recomendación de la empresa actual", 1, 80, 10)
    input_politicas_diversidad = st.slider("Nivel de políticas de diversidad en la empresa actual", 1, 80, 10)
    input_pandemia_percepcion = st.slider("Percepción de la pandemia", 1, 80, 10)

# with c2:


with st.echo(code_location='below'):








    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = input_edad / input_experiencia_anios

    for curr_point_num in range(input_edad):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / input_edad
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
