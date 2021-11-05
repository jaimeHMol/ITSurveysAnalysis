import os
from pathlib import Path

from data_process import DataProcess

project_path = Path(os.getcwd())
output_path = project_path / "data/prepared/"


# ----------------------------------------------------------------------------------
# Data load
sysarmy_survey = project_path / "data/raw/2021.2 - sysarmy - Encuesta de remuneración salarial Argentina.csv"
sysarmy_analysis = DataProcess(sysarmy_survey, "csv")


# ----------------------------------------------------------------------------------
# Data refine and exploration
print(sysarmy_analysis)

# Columns from 2020
# cols_to_remove = [
#     "Estoy trabajando en",
#     "Años en el puesto actual",
#     "Cuánto cobrás por guardia",
#     "¿Porcentaje, bruto o neto?",                  
#     "Salario mensual NETO (en tu moneda local)",
#     "Cómo creés que está tu sueldo con respecto al último semestre",
#     "A qué está atado el bono",
#     "¿Tenés algún tipo de discapacidad?",
#     "¿Sentís que esto te dificultó el conseguir trabajo?",
#     "¿En qué mes fue el último ajuste?",
#     "Beneficios extra",   
#     "¿Cuáles considerás que son las mejores empresas de IT para trabajar en este momento, en tu ciudad?",
#     "QA / Testing",
#     "Sueldo dolarizado?",
#     "Trabajo de", # Don"t remove if you want to do a gender analysis
#     "Orientación sexual", # Don"t remove if you want to do a diversity analysis
#     "Carrera",
#     "Universidad",
# ]
cols_to_remove = [
    "Dónde estás trabajando",
    "Salario mensual o retiro NETO (en tu moneda local)",
    "Pagos en dólares",
    "¿Cuál fue el último valor de dólar que tomaron?",
    "Cómo creés que está tu sueldo con respecto al último semestre",
    "A qué está atado el bono",
    "¿En qué mes fue el último ajuste?",
    "Trabajo de", # Don"t remove if you want to do a gender analysis
    "Años en el puesto actual",
    "QA / Testing",
    "Cantidad de personas en tu organización",
    "Trabajo para una empresa que no tiene oficina en mi ciudad",
    "Actividad principal",
    "Beneficios extra",
    "¿Salir o seguir contestando?", # Could be useful
    "¿Salir o seguir contestando?.1", # Could be useful
    "Carrera",
    "Universidad",
    "Cuánto cobrás por guardia",
    "¿Porcentaje, bruto o neto?",
    "¿Salir o seguir contestando?.2", # Could be useful
    "¿Tenés algún tipo de discapacidad?",
    "¿Sentís que esto te dificultó el conseguir trabajo?",
    "¿Salir o seguir contestando?.3", # Could be useful
    "¿Tenés hijos/as menores de edad?", # Could be useful
    "¿Con cuántas personas estás conviviendo?", # Could be useful
    "¿Con quiénes convivís?", # Could be useful
    "¿Tenés un espacio dedicado para el trabajo?", # Could be useful
    "¿Tenés que compartir tu equipo de trabajo con alguien?", # Could be useful
    "¿Qué tipo de cuarentena hiciste / estás haciendo?", # Could be useful
    "¿Cambió tu situación laboral a raíz de la pandemia?", # Could be useful
    "¿Qué tanto sentís que te está apoyando tu empresa/organización en esta situación?", # Could be useful
    "¿Cómo se vio afectada tu empresa/organización?", # Could be useful
    "¿Instauraron algún beneficio nuevo?", # Could be useful
]

sysarmy_analysis.remove_cols(cols_to_remove)
print(sysarmy_analysis)

# Column mapping from 2020
# cols_to_rename = {
#     "Me identifico": "genero",
#     "Tengo": "edad",
#     "Dónde estás trabajando": "ubicacion",
#     "Tipo de contrato": "tipo_contrato",
#     "Años de experiencia": "experiencia_anios",
#     "Años en la empresa actual": "empresa_actual_anios",
#     "Nivel de estudios alcanzado": "max_nivel_estudios",
#     "¿Gente a cargo?": "personas_a_cargo",
#     "Estado": "max_nivel_estudios_estado",
#     "Realizaste cursos de especialización": "cursos_especializacion",
#     "¿Contribuís a proyectos open source?": "contribucion_open_source",
#     "¿Programás como hobbie?": "programacion_hobbie",
#     # "Trabajo de": "rol_trabajo",
#     "¿Qué SO usás en tu laptop/PC para trabajar?": "computador_trabajo_so",
#     "¿Y en tu celular?": "celular_so",
#     "¿Tenés guardias?": "guardias",
#     "Salario mensual BRUTO (en tu moneda local)": "sueldo_mensual_bruto_ars",
#     # "Sueldo dolarizado?": "sueldo_dolarizado",
#     "¿Qué tan conforme estás con tu sueldo?": "sueldo_conformidad",
#     "Recibís algún tipo de bono": "sueldo_bonos",
#     "¿Tuviste ajustes por inflación en lo que va de 2020?": "sueldo_ajustes_inflacion",
#     "¿De qué % fue el ajuste total?": "sueldo_ajuste_total_2020",
#     "¿Sufriste o presenciaste situaciones de violencia laboral?": "violencia_laboral",
#     "¿La recomendás como un buen lugar para trabajar?": "recomendacion_laboral",
#     "¿Cómo calificás las políticas de diversidad e inclusión?": "politicas_diversidad",
# }
cols_to_rename = {
    "Me identifico": "genero",
    "Tengo": "edad",
    "Dónde estás trabajando": "ubicacion",
    "Tipo de contrato": "tipo_contrato",
    "Años de experiencia": "experiencia_anios",
    "Años en la empresa actual": "empresa_actual_anios",
    "Nivel de estudios alcanzado": "max_nivel_estudios",
    "¿Gente a cargo?": "personas_a_cargo",
    "Estado": "max_nivel_estudios_estado",
    "Realizaste cursos de especialización": "cursos_especializacion",
    "¿Contribuís a proyectos open source?": "contribucion_open_source",
    "¿Programás como hobbie?": "programacion_hobbie",
    # "Trabajo de": "rol_trabajo",
    "¿Qué SO usás en tu laptop/PC para trabajar?": "computador_trabajo_so",
    "¿Y en tu celular?": "celular_so",
    "¿Tenés guardias?": "guardias",
    "Salario mensual BRUTO (en tu moneda local)": "sueldo_mensual_bruto_ars",
    # "Sueldo dolarizado?": "sueldo_dolarizado",
    "¿Qué tan conforme estás con tu sueldo?": "sueldo_conformidad",
    "Recibís algún tipo de bono": "sueldo_bonos",
    "¿Tuviste ajustes por inflación en lo que va de 2021?": "sueldo_ajustes_inflacion",
    "¿De qué % fue el ajuste total?": "sueldo_ajuste_total_2021",
    "¿Sufriste o presenciaste situaciones de violencia laboral?": "violencia_laboral",
    "¿La recomendás como un buen lugar para trabajar?": "recomendacion_laboral",
    "¿Cómo calificás las políticas de diversidad e inclusión?": "politicas_diversidad",
    "¿Cómo venís llevando la pandemia?": "pandemia_feeling",
}

sysarmy_analysis.rename_cols(cols_to_rename)
print(sysarmy_analysis)
# sysarmy_analysis.describe(graph=True)

numeric_types = ["int32", "int64", "float32", "float64"]
cols_by_type = sysarmy_analysis.group_cols_by_type()
cols_numeric = sysarmy_analysis.get_cols_by_type(cols_by_type, numeric_types)

cols_to_unify = [
    "Plataformas",
    "Lenguajes de programación o tecnologías.", 
    "Frameworks, herramientas y librerías",
    "Bases de datos",
    "IDEs"
]
str_to_replace = {
    "ninguna de las anteriores": "", 
    "ninguno de los anteriores": "",
    "ninguno": "", 
    "ninguna": "",
    "microsoft": "",
    "oracle": "",
    "ibm": "",
    "saleforce": "",
    "google": "",
    "apache": "",
    "; ": ",", 
    ";": "", 
    ".": "", 
    ", ": ",", 
    " ": "",
    "-":"",
    "0":"",
}
sysarmy_analysis.unify_cols(cols_to_unify, "tecnologies", str_to_replace)

sysarmy_analysis.remove_cols(cols_to_unify)

# sysarmy_analysis.explore()
sysarmy_analysis.describe(graph=True)

all_cols = list(sysarmy_analysis.dataset.columns)
sysarmy_analysis.replace_missing(all_cols, method="remove")

# Remove column with special case
cols_numeric.remove("personas_a_cargo")
sysarmy_analysis.replace_outliers(cols_numeric, method="drop_iqr")
sysarmy_analysis.replace_outliers(["personas_a_cargo"], method="drop_5_95")
cols_numeric.append("personas_a_cargo")

sysarmy_analysis.describe(graph=True)
# Careful with the variables "presonas_a_cargo", "sueldo_ajuste_total_2020"
            
# ----------------------------------------------------------------------------------
# Data processing
all_cols_to_standard = cols_numeric

cols_to_standard = [
    "edad", 
    "experiencia_anios" ,
    "empresa_actual_anios", 
    "personas_a_cargo",
    "sueldo_conformidad",
    "sueldo_mensual_bruto_ars",
    "sueldo_ajuste_total_2020",
    "recomendacion_laboral",
    "politicas_diversidad"
]
sysarmy_analysis.standardize(cols_to_standard, "z_score")

# Dimensionality reduction using PCA:
# Applies only for numeric columns, requieres standardized values
sysarmy_analysis.reduction_dims(
    cols_to_standard,
    method="pca", 
    final_number_dims=2, 
    visualize=True
)

sysarmy_analysis.clusterization(
    cols_to_standard,
    method="dbscan", 
    visualize=True
)

sysarmy_analysis.dummy_cols_from_text(col="tecnologies", sep=",", n_cols=15)
print(sysarmy_analysis)



import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
# import statsmodels.api as sm

var_to_predict = "sueldo_mensual_bruto_ars"
xs = sysarmy_analysis.dataset.drop([var_to_predict], axis=1)

cols_by_type = sysarmy_analysis.group_cols_by_type()
cols_numeric = sysarmy_analysis.get_cols_by_type(cols_by_type, numeric_types)
cols_numeric.remove(var_to_predict)
cols_numeric.remove("PC1")
cols_numeric.remove("PC2")

y = sysarmy_analysis.dataset[var_to_predict]
reg = LinearRegression()
reg.fit(xs[cols_numeric], y)
print("")
print("R2 coefficient: ")
print(reg.score(xs[cols_numeric], y))

# get importance
importance = reg.coef_
# summarize feature importance. # TODO: Use features names.
for i,v in enumerate(importance):
	print("Feature: %0d, Score: %.5f" % (i,v))
# plot feature importance
plt.bar([x for x in range(len(importance))], importance)
plt.show()


# ----------------------------------------------------------------------------------
# sysarmy_analysis.reset()
# print(sysarmy_analysis)

# sysarmy_analysis.save(output_path / "sysarmy_survey_analysed.csv")
# print(sysarmy_analysis)
