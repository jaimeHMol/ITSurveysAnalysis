import math
from collections import namedtuple

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Predictor de salarios.",
    page_icon="💸",
)

with st.sidebar:
    st.markdown("### Variables del modelo")
    input_edad = st.slider("Edad", 15, 70, 15)
    input_experiencia_anios = st.slider("Experiencia en años", 0, 50, 0)
    input_empresa_actual_anios = st.slider("Tiempo en empresa actual en años", 0, 50, 0)
    input_personas_a_cargo = st.slider("Personas a cargo", 0, 100, 0)
    input_sueldo_ajuste_total_2021 = st.slider("Porcentaje total de ajuste del sueldo en 2021", 0, 100, 0)
    input_recomendacion_laboral = st.slider("Nivel de recomendación de la empresa actual", 0, 10, 5)
    input_politicas_diversidad = st.slider("Nivel de políticas de diversidad en la empresa actual", 0, 10, 5)
    input_genero = st.selectbox("Genero", ["Femenino", "Masculino", "Otro", "No Responde"])
    input_contribucion_open_source = st.selectbox("Contribución Open Source", ("Si", "No", "No Responde"))
    input_cursos_especializacion = st.selectbox("Cursos de especialización", ("Si", "No", "No Responde"))
    input_guardias = st.selectbox("Tienes guardias", ("No", "Si, activa",  "Si, pasiva"))
    input_max_nivel_estudios = st.selectbox("Nivel máximo de estudios alcanzado", ("Primario", "Secundario", "Terciario", "Universitario", "Posgrado", "Doctorado", "Posdoctorado", "No Responde"))
    input_programacion_hobbie = st.selectbox("Programas como hobbie?", ("Si", "No", "No Responde"))
    input_sueldo_ajuste_2021 = st.selectbox("Cuantos ajustes de sueldo tuviste durante el 2021?", ("Ninguno", "Uno", "Dos", "Tres", "Más de tres"))
    input_sueldo_bonos = st.selectbox("Recibes bonos adicionales al sueldo?", ("Menos de un sueldo", "Un sueldo", "De uno a tres sueldos", "Más de tres sueldos", "No"))
    input_tipo_contrato = st.selectbox("Que tipo de contrato tienes?", ("Full-Time", "Part-Time", "Remoto", "Tercerizado", "Freelance", "Participación societaria en cooperativa"))
    input_violencia_laboral = st.selectbox("Has vivido violencia laboral?", ("Jamás", "En mi trabajo actual", "En un trabajo anterior", "No responde"))


    options = st.multiselect(
        "Qué tecnologías dominas?",
        ["amazonwebservices", "css", "docker", "html", "java", "javascript", "linux", "mysql", "nodejs", "postgresql", "python", "reactjs", "sql", "sqlserver", "visualstudiocode"],
    )

"""
# Predictor de sueldos en TI

Hola, aquí podrás obtener una predicción del sueldo bruto mensual en pesos argentinos que 
ganarías según el valor de las 18 variables de entrada que puedes ingresar en el panel 
desplegable de la izquierda.

Los modelos regresores se realizaron tomando como base los datos de la encuesta de sueldos
llevada a cabo por la comunidad de sysarmy en el segundo semestre del 2021.

Para obtener más detalles del modelo implementado puedes entrar [aquí](https://www.jaimehmol.me).

@jaimehmol
<br>


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





# with st.echo(code_location="below"):
#     Point = namedtuple("Point", "x y")
#     data = []

#     points_per_turn = input_edad / input_experiencia_anios

#     for curr_point_num in range(input_edad):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / input_edad
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color="#0068c9", opacity=0.5)
#         .encode(x="x:Q", y="y:Q"))
