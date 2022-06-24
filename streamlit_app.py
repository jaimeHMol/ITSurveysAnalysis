import os
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
from joblib import load

st.set_page_config(
    page_title="Predictor de salarios.",
    page_icon="💸",
)

project_path = Path(os.getcwd())
export_path = project_path / "export/"

# Import model and transformations to be applied on the input data
scaler_y = load(export_path / "export_scaler_output.joblib")
scaler_X = load(export_path / "export_scaler_input.joblib")

# st.session_state.run_id = 1

def clear_inputs():
    # run_id += 1
    # st.session_state.run_id += 1
    st.session_state["input_edad"] = 15
    st.session_state["input_experiencia_anios"] = 0
    st.session_state["input_empresa_actual_anios"] = 0
    st.session_state["input_personas_a_cargo"] = 0
    st.session_state["input_sueldo_ajuste_total_2021"] = 0
    st.session_state["input_recomendacion_laboral"] = 5
    st.session_state["input_politicas_diversidad"] = 5
    # st.session_state.input_genero = ()
    # st.session_state["input_genero"] = ""
    # st.session_state["input_contribucion_open_source"] = ""
    # st.session_state["input_cursos_especializacion"] = ""
    # st.session_state["input_guardias"] = ""
    # st.session_state["input_max_nivel_estudios"] = ""
    # st.session_state["input_programacion_hobbie"] = ""
    # st.session_state["input_sueldo_ajuste_2021"] = ""
    # st.session_state["input_sueldo_bonos"] = ""
    # st.session_state["input_tipo_contrato"] = ""
    # st.session_state["input_violencia_laboral"] = ""
    st.session_state["input_tecnologias"] = []
    return


def predict_salary(model_type):
    if model_type == "Linear Regression Ridge":
        model = load(export_path / "export_linear_regression_ridge.joblib")
    elif model_type == "Random Forest":
        model = load(export_path / "export_random_forest.joblib")

    # return model.predict()
    return scaler_y.transform([input_personas_a_cargo])


with st.sidebar:
    # run_id = st.session_state.run_id
    st.markdown("### Variables del modelo")
    input_edad = st.slider("Edad", 15, 70, 15, key="input_edad")
    input_experiencia_anios = st.slider("Experiencia en años", 0, 50, 0, key="input_experiencia_anios")
    input_empresa_actual_anios = st.slider("Tiempo en empresa actual en años", 0, 50, 0, key="input_empresa_actual_anios")
    input_personas_a_cargo = st.slider("Personas a cargo", 0, 100, 0, key="input_personas_a_cargo")
    input_sueldo_ajuste_total_2021 = st.slider("Porcentaje total de ajuste del sueldo en 2021", 0, 100, 0, key="input_sueldo_ajuste_total_2021")
    input_recomendacion_laboral = st.slider("Nivel de recomendación de la empresa actual", 0, 10, 5, key="input_recomendacion_laboral")
    input_politicas_diversidad = st.slider("Nivel de políticas de diversidad en la empresa actual", 0, 10, 5, key="input_politicas_diversidad")
    input_genero = st.selectbox("Genero", ["Femenino", "Masculino", "Otro", "No Responde"], key="input_genero")
    input_contribucion_open_source = st.selectbox("Contribución Open Source", ("Si", "No", "No Responde"), key="input_contribucion_open_source")
    input_cursos_especializacion = st.selectbox("Cursos de especialización", ("Si", "No", "No Responde"), key="input_cursos_especializacion")
    input_guardias = st.selectbox("Tienes guardias", ("No", "Si, activa",  "Si, pasiva"), key="input_guardias")
    input_max_nivel_estudios = st.selectbox("Nivel máximo de estudios alcanzado", ("Primario", "Secundario", "Terciario", "Universitario", "Posgrado", "Doctorado", "Posdoctorado", "No Responde"), key="input_max_nivel_estudios")
    input_programacion_hobbie = st.selectbox("Programas como hobbie?", ("Si", "No", "No Responde"), key="input_programacion_hobbie")
    input_sueldo_ajuste_2021 = st.selectbox("Cuantos ajustes de sueldo tuviste durante el 2021?", ("Ninguno", "Uno", "Dos", "Tres", "Más de tres"), key="input_sueldo_ajuste_2021")
    input_sueldo_bonos = st.selectbox("Recibes bonos adicionales al sueldo?", ("No", "Menos de un sueldo", "Un sueldo", "De uno a tres sueldos", "Más de tres sueldos"), key="input_sueldo_bonos")
    input_tipo_contrato = st.selectbox("Que tipo de contrato tienes?", ("Full-Time", "Part-Time", "Remoto", "Tercerizado", "Freelance", "Participación societaria en cooperativa"), key="input_tipo_contrato")
    input_violencia_laboral = st.selectbox("Has vivido violencia laboral?", ("Jamás", "En mi trabajo actual", "En un trabajo anterior", "No responde"), key="input_violencia_laboral")
    input_tecnologias = st.multiselect(
        "Qué tecnologías dominas?",
        ["amazonwebservices", "css", "docker", "html", "java", "javascript", "linux", "mysql", "nodejs", "postgresql", "python", "reactjs", "sql", "sqlserver", "visualstudiocode"],
        key="input_tecnologias",
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
    model_type = st.radio(
        "Choose your model",
        ["Linear Regression Ridge", "Random Forest"],
        help="At present, you can choose between 2 models (Linear Regression or \
        Random Forest) to predict the salary.",
    )
    predict = st.form_submit_button("Predecir")
    if predict:
        predicted_salary = predict_salary(model_type)
        st.write(f"Tu sueldo esperado debería ser: {predicted_salary} pesos argentinos (ARS)")

st.button("Limpiar entradas", on_click=clear_inputs)
