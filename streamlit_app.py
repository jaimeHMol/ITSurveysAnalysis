import math
from collections import namedtuple

import altair as alt
import pandas as pd
import streamlit as st
from numpy import ones_like

st.set_page_config(
    page_title="Predictor de salarios.",
    page_icon="💸",
)

st.session_state["run_id"] = 1

def clear_inputs():
    # run_id += 1
    st.session_state["run_id"] += 1

    # st.session_state["input_edad"] = 15
    # st.session_state["input_experiencia_anios"] = 0
    # st.session_state["input_empresa_actual_anios"] = 0
    # st.session_state["input_personas_a_cargo"] = 0
    # st.session_state["input_sueldo_ajuste_total_2021"] = 0
    # st.session_state["input_recomendacion_laboral"] = 5
    # st.session_state["input_politicas_diversidad"] = 5
    # # st.session_state.input_genero = ()
    # # st.session_state["input_genero"] = ""
    # # st.session_state["input_contribucion_open_source"] = ""
    # # st.session_state["input_cursos_especializacion"] = ""
    # # st.session_state["input_guardias"] = ""
    # # st.session_state["input_max_nivel_estudios"] = ""
    # # st.session_state["input_programacion_hobbie"] = ""
    # # st.session_state["input_sueldo_ajuste_2021"] = ""
    # # st.session_state["input_sueldo_bonos"] = ""
    # # st.session_state["input_tipo_contrato"] = ""
    # # st.session_state["input_violencia_laboral"] = ""
    # st.session_state.input_tecnologias = []
    # return


with st.sidebar:
    run_id = st.session_state["run_id"]
    st.markdown("### Variables del modelo")
    input_edad = st.slider("Edad", 15, 70, 15, key=f"input_edad{run_id}")
    input_experiencia_anios = st.slider("Experiencia en años", 0, 50, 0, key=f"input_experiencia_anios{run_id}")
    input_empresa_actual_anios = st.slider("Tiempo en empresa actual en años", 0, 50, 0, key=f"input_empresa_actual_anios{run_id}")
    input_personas_a_cargo = st.slider("Personas a cargo", 0, 100, 0, key=f"input_personas_a_cargo{run_id}")
    input_sueldo_ajuste_total_2021 = st.slider("Porcentaje total de ajuste del sueldo en 2021", 0, 100, 0, key=f"input_sueldo_ajuste_total_2021{run_id}")
    input_recomendacion_laboral = st.slider("Nivel de recomendación de la empresa actual", 0, 10, 5, key=f"input_recomendacion_laboral{run_id}")
    input_politicas_diversidad = st.slider("Nivel de políticas de diversidad en la empresa actual", 0, 10, 5, key=f"input_politicas_diversidad{run_id}")
    input_genero = st.selectbox("Genero", ["Femenino", "Masculino", "Otro", "No Responde"], key=f"input_genero{run_id}")
    input_contribucion_open_source = st.selectbox("Contribución Open Source", ("Si", "No", "No Responde"), key=f"input_contribucion_open_source{run_id}")
    input_cursos_especializacion = st.selectbox("Cursos de especialización", ("Si", "No", "No Responde"), key=f"input_cursos_especializacion{run_id}")
    input_guardias = st.selectbox("Tienes guardias", ("No", "Si, activa",  "Si, pasiva"), key=f"input_guardias{run_id}")
    input_max_nivel_estudios = st.selectbox("Nivel máximo de estudios alcanzado", ("Primario", "Secundario", "Terciario", "Universitario", "Posgrado", "Doctorado", "Posdoctorado", "No Responde"), key=f"input_max_nivel_estudios{run_id}")
    input_programacion_hobbie = st.selectbox("Programas como hobbie?", ("Si", "No", "No Responde"), key=f"input_programacion_hobbie{run_id}")
    input_sueldo_ajuste_2021 = st.selectbox("Cuantos ajustes de sueldo tuviste durante el 2021?", ("Ninguno", "Uno", "Dos", "Tres", "Más de tres"), key=f"input_sueldo_ajuste_2021{run_id}")
    input_sueldo_bonos = st.selectbox("Recibes bonos adicionales al sueldo?", ("No", "Menos de un sueldo", "Un sueldo", "De uno a tres sueldos", "Más de tres sueldos"), key=f"input_sueldo_bonos{run_id}")
    input_tipo_contrato = st.selectbox("Que tipo de contrato tienes?", ("Full-Time", "Part-Time", "Remoto", "Tercerizado", "Freelance", "Participación societaria en cooperativa"), key=f"input_tipo_contrato{run_id}")
    input_violencia_laboral = st.selectbox("Has vivido violencia laboral?", ("Jamás", "En mi trabajo actual", "En un trabajo anterior", "No responde"), key=f"input_violencia_laboral{run_id}")
    input_tecnologias = st.multiselect(
        "Qué tecnologías dominas?",
        ["amazonwebservices", "css", "docker", "html", "java", "javascript", "linux", "mysql", "nodejs", "postgresql", "python", "reactjs", "sql", "sqlserver", "visualstudiocode"],
        key=f"input_tecnologias{run_id}",
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
"""
st.write("###")

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

st.button("Limpiar entradas", on_click=clear_inputs)
