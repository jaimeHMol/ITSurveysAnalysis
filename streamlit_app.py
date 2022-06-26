import os
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from joblib import load

import mappings as maps

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

    X_input = arrange_inputs()
    X_to_predict = scaler_X.transform([X_input])
    y_predict_scaled = model.predict([X_to_predict])
    y_predict = scaler_y.inverse_transform([np.float_(y_predict_scaled)])[0]
    return X_input

    # return y_predict
    # return scaler_y.inverse_transform([np.float_(input_personas_a_cargo)])[0]


def arrange_inputs():
    selection_genero = transpose_list_of_values(maps.genero, [input_genero])
    selection_contribucion_open_source = transpose_list_of_values(maps.contribucion_open_source, [input_contribucion_open_source])
    selection_cursos_especializacion = transpose_list_of_values(maps.cursos_especializacion, [input_cursos_especializacion])
    selection_guardias = transpose_list_of_values(maps.guardias, [input_guardias])
    selection_max_nivel_estudios = transpose_list_of_values(maps.max_nivel_estudios, [input_max_nivel_estudios])
    selection_programacion_hobbie = transpose_list_of_values(maps.programacion_hobbie, [input_programacion_hobbie])
    selection_sueldo_ajuste_2021 = transpose_list_of_values(maps.sueldo_ajuste_2021, [input_sueldo_ajuste_2021])
    selection_sueldo_bonos = transpose_list_of_values(maps.sueldo_bonos, [input_sueldo_bonos])
    selection_tipo_contrato = transpose_list_of_values(maps.tipo_contrato, [input_tipo_contrato])
    selection_violencia_laboral = transpose_list_of_values(maps.violencia_laboral, [input_violencia_laboral])
    selection_tecnologias = transpose_list_of_values(maps.tecnologias, input_tecnologias)
    
    X_input = [input_edad] + [input_experiencia_anios] + [input_empresa_actual_anios] \
    + [input_personas_a_cargo] + [input_sueldo_ajuste_total_2021] \
    + [input_recomendacion_laboral] + [input_politicas_diversidad] + selection_genero \
    + selection_contribucion_open_source + selection_cursos_especializacion \
    + selection_guardias + selection_max_nivel_estudios + selection_programacion_hobbie \
    + selection_sueldo_ajuste_2021 + selection_sueldo_bonos + selection_tipo_contrato \
    + selection_violencia_laboral + selection_tecnologias
    return X_input


def transpose_list_of_values(list_of_values, selected_values):
    output_list = [0 for _ in range(len(list_of_values))]
    for selected_value in selected_values:
        index = list_of_values.index(selected_value)
        output_list[index] = 1
    return output_list


# Create the sidebar with all the input variables for the predictive model
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
    input_genero = st.selectbox("Genero", maps.genero, key="input_genero")
    input_contribucion_open_source = st.selectbox("Contribución Open Source", maps.contribucion_open_source, key="input_contribucion_open_source")
    input_cursos_especializacion = st.selectbox("Cursos de especialización", maps.cursos_especializacion, key="input_cursos_especializacion")
    input_guardias = st.selectbox("Tienes guardias", maps.guardias, key="input_guardias")
    input_max_nivel_estudios = st.selectbox("Nivel máximo de estudios alcanzado", maps.max_nivel_estudios, key="input_max_nivel_estudios")
    input_programacion_hobbie = st.selectbox("Programas como hobbie?", maps.programacion_hobbie, key="input_programacion_hobbie")
    input_sueldo_ajuste_2021 = st.selectbox("Cuantos ajustes de sueldo tuviste durante el 2021?", maps.sueldo_ajuste_2021, key="input_sueldo_ajuste_2021")
    input_sueldo_bonos = st.selectbox("Recibes bonos adicionales al sueldo?", maps.sueldo_bonos, key="input_sueldo_bonos")
    input_tipo_contrato = st.selectbox("Que tipo de contrato tienes?", maps.tipo_contrato, key="input_tipo_contrato")
    input_violencia_laboral = st.selectbox("Has vivido violencia laboral?", maps.violencia_laboral, key="input_violencia_laboral")
    input_tecnologias = st.multiselect("Qué tecnologías dominas?", maps.tecnologias, key="input_tecnologias")


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
