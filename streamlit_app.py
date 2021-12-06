import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Bienvenido al predictor de sueldos en TI

Hola, aquí podrás obtener una predicción del sueldo bruto mensual en pesos argentinos que 
ganarías según el valor de XXX variables de entrada.

Esta regresión se realizó tomando como base los datos de la encuesta de sueldos llevada a 
cabo por la comunidad de sysarmy en el segundo semestre del 2021.

Para obtener más detalles del modelo implementado puedes entrar [aquí](https://www.jaimehmol.me).

@jaimehmol
"""


with st.echo(code_location='below'):
    input_edad = st.slider("Edad", 1, 80, 10)
    input_experiencia_anios = st.slider("Experiencia en años", 1, 80, 10)
    input_empresa_actual_anios = st.slider("Tiempo en empresa actual en años", 1, 80, 10)
    input_personas_a_cargo = st.slider("Personas a cargo", 1, 80, 10)
    input_sueldo_ajuste_total_2021 = st.slider("Ajuste de sueldo total en 2021", 1, 80, 10)
    input_recomendacion_laboral = st.slider("Nivel de recomendación de la empresa actual", 1, 80, 10)
    input_politicas_diversidad = st.slider("Nivel de políticas de diversidad en la empresa actual", 1, 80, 10)
    input_pandemia_percepcion = st.slider("Percepción de la pandemia", 1, 80, 10)

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