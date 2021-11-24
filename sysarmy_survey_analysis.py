import os
from pathlib import Path
import numpy as np

from data_process import DataProcess

project_path = Path(os.getcwd())
output_path = project_path / "data/prepared/"
USD_ARS = 105

# ----------------------------------------------------------------------------------
# Data load
sysarmy_survey = project_path / "data/raw/2021.2 - sysarmy - Encuesta de remuneración salarial Argentina.csv"
sysarmy_analysis = DataProcess(sysarmy_survey, "csv")


# ----------------------------------------------------------------------------------
# Data refine and exploration
print(sysarmy_analysis)

cols_to_drop = [
    "Dónde estás trabajando",
    "Salario mensual o retiro NETO (en tu moneda local)",
    "Pagos en dólares",
    "¿Cuál fue el último valor de dólar que tomaron?",
    "Cómo creés que está tu sueldo con respecto al último semestre",
    "A qué está atado el bono",
    "¿En qué mes fue el último ajuste?",
    "Trabajo de", # Don"t drop if you want to do a gender analysis
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
    "Unnamed: 60",
    "Unnamed: 61",
    "Unnamed: 62",
    "Unnamed: 63",
    "Unnamed: 64",
    "Unnamed: 65",
]
sysarmy_analysis.drop_cols(cols_to_drop)
print(sysarmy_analysis)

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
    "Salario mensual o retiro BRUTO (en tu moneda local)": "sueldo_mensual_bruto_ars",
    # "Sueldo dolarizado?": "sueldo_dolarizado",
    "¿Tuviste ajustes por inflación durante 2021?": "sueldo_ajuste_2021",
    "¿Qué tan conforme estás con tu sueldo?": "sueldo_conformidad",
    "Recibís algún tipo de bono": "sueldo_bonos",
    "¿Tuviste ajustes por inflación en lo que va de 2021?": "sueldo_ajustes_inflacion",
    "¿De qué % fue el ajuste total?": "sueldo_ajuste_total_2021",
    "¿Sufriste o presenciaste situaciones de violencia laboral?": "violencia_laboral",
    "¿La recomendás como un buen lugar para trabajar?": "recomendacion_laboral",
    "¿Cómo calificás las políticas de diversidad e inclusión?": "politicas_diversidad",
    "¿Cómo venís llevando la pandemia?": "pandemia_percepcion",
}
sysarmy_analysis.rename_cols(cols_to_rename)

sysarmy_analysis.enforce_numeric(["sueldo_mensual_bruto_ars"])

print(sysarmy_analysis)
# sysarmy_analysis.describe(graph=True)

numeric_types = ["int8", "int16", "int32", "int64", "float8", "float16", "float32", "float64"]
cols_by_type = sysarmy_analysis.group_cols_by_type()
cols_numeric = sysarmy_analysis.get_cols_by_type(cols_by_type, numeric_types)

# Create tecnologies column unifying multiple related columns
cols_to_unify = [
    "Plataformas",
    "Lenguajes de programación o tecnologías.", 
    "Frameworks, herramientas y librerías",
    "Bases de datos",
    "IDEs"
]
tecs_to_replace = {
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
sysarmy_analysis.unify_cols(cols_to_unify, "tecnologies", tecs_to_replace)
sysarmy_analysis.drop_cols(cols_to_unify)

# Unify the multiple ways to referer to the gender, since the goal of this analysis is
# focus on the salary but not in diversity.
genders_to_replace = {
    "Varón (Supongo que Cis, no se que significa)": "Masculino",
    "Varon heterosexual de pelo en pecho no entiendo que es cis corrigan eso": "Masculino",
    "Varon Heterosexual blanco, Agorista, Anarquista, Liberal": "Masculino",
    "Hombre. Punto. 🤦🏻\u200d♂️ Son impresentable con este punto ": "Masculino",
    "Me rompe los huevos estas opciones. Soy masculino": "Masculino",
    "no se entiendo! Soy hombre, heterosexual y  me gustan las minas": "Masculino",
    "Hombre (hay solo 2 generos biologicos y no deberian discriminar por preferencias sexuales, no aporta al supuesto gender pay gap)": "Masculino",
    "biológicamente hombre": "Masculino",
    "wtf es esto? hombre": "Masculino",
    "Macho lomo plateado": "Masculino",
    "Masculino macho": "Masculino",
    "Varon la puta madre": "Masculino",
    "Hombre normal heterosexual": "Masculino",
    "Hombre heterosexual": "Masculino",
    "Hombre Heterosexual": "Masculino",
    "Masculino no pregunten pendejadas": "Masculino",
    "Varon, a secas, me gustan las mujeres, cortemos con la boludes": "Masculino",
    "que pelotudos, soy masculino": "Masculino",
    "Hombre nada de Cis ": "Masculino",
    "Me indentifico como Masculino, uno de los dos sexos que existen.": "Masculino",
    "varon heterosexual ": "Masculino",
    "Varon heterosexual": "Masculino",
    "Hombre, no inventen boludeces": "Masculino",
    "Hombre, zurdos pelotudos no inventen la rueda": "Masculino",
    "una ridiculez esta pregunta. Me es difícil entender donde poner que soy HOMBRE": "Masculino",
    "Hombre, man, ¿qué son todos esos términos? ": "Masculino",
    'Para q preguntan esto??? Que tiene q ver??? Nací con pito, por eso soy hombre. Tan dificil es??? Ademas, a quien le importa como te "identificas"???': "Masculino",
    '"Que le fue asignado al nacer"?? WTF? Tengo pito y me gustan las chicas. Lo que hace miles de años se conocía como: Hombre': "Masculino",
    "Macho alfa estilo cosaco": "Masculino",
    "El varon comun y corriente. No se que opcion es": "Masculino",
    "Que es todo esto? Tengo huevos y me gustan las mujeres.": "Masculino",
    "Hombre bisexual": "Masculino",
    "Masculino y punto": "Masculino",
    "soy hombre LRPMQTP": "Masculino",
    "Helicoptero apache (nah mentira, soy hombre)": "Masculino",
    "Mujer/Fememino/Humano hembra. No se cual opción de arriba sería.": "Femenino",
    "MUJER SEXO FEMENINO DEJENSE DE JODER CON GENERO, ES SEXO!!! EN DONDE VAMOS A TERMINAR CON ESTAS PAVADAS DIO MIO!!!": "Femenino",
    "Mujer ¯\\_(ツ)_/¯ ·": "Femenino",
    "UNA PERONOLA GIRANDO EN CUATRO DIMENSIONES": "No responde",
    "Tortuga Ninja": "No responde",
    "Prefiero no decir": "No responde",
    "Ni idea, no le doy hola a esas cosas.": "No responde",
    "Deberian colocar ademas de todo lo incluyente el clasico hombre y mujer": "No responde",
    "alienigena.. que carajo es esto? en serio.": "No responde",
    "no se que significa cada opción, así que no se": "No responde",
    "Me identifico por mi nombre y apellido.": "No responde",
    "Me autopercibo jirafa": "No responde",
    "Chupala": "No responde",
    "Normal, no raro como otros": "No responde",
    "no me interesa los cartelitos": "No responde",
    "Que quilombo esto de los generos": "No responde",
    "No entiendo esta pregunta": "No responde",
    "Un galline no binario": "No responde",
    "ESTO ES DISCRIMINAR, NO SE PUEDE UTILIZAR ESTA INFORMACIÓN PARA GENERAR ESTADISTICAS": "No responde",
    "QUE PREGUNTA PELOTUDA": "No responde",
    "really? siguen con esta boludez?": "No responde",
    "que es esto????": "No responde",
    "helicoptero de ataque": "No responde",
    "helicóptero de combate": "No responde",
    "Helicóptero de combate": "No responde",
    "Helicoptero de combate": "No responde",
    "Que ganas de joder con estas pavadas :P": "No responde",
    "Algunos días como salame": "No responde",
    "que carajo es CIS? estan locos? sales de la panza y te ponen el genero?? esto se sale de control!!!": "No responde",
    "basta de boludeces": "No responde",
    "Que tiene que ver": "No responde",
    "Es complicado": "No responde",
    "Solo hay 2 sexos hombre o mujer.": "No responde",
    "Esto es una mierda": "No responde",
    "Casi Normal": "No responde",
    "Un ornitorrinco pelotudos": "No responde",
    "naaaaaaaaaaaaaaaaaaaaaaaaa": "No responde",
    "Yo soy un pollo Marge!": "No responde",
    "Solo hay 2 sexos hombre o mujer.": "No responde",
    "furro (no hay pregunta más estúpida que ésta? acaso les paga algún colectivo LGTBQI? jajaja": "No responde",
    "JAJAJAJA seriedad por favor....": "No responde",
    "alienigena.. que carajo es estoOtro en serio.": "No responde",
    "non binarie plus lgbt q + system.debug": "No responde",
    "Sapiosexual (Bi).": "No responde",
    "Que pelotudes": "No responde",
    "Chevy camaro": "No responde",
    "Cis? O sea no quieren etiquetas y me tengo que poner una etiqueta": "No responde",
    "No entiendo": "No responde",
    "Helicóptero Apache": "No responde",
    "Dejen de pelotudear con estás pijas": "No responde",
    "Oso panda rengo": "No responde",
    "muy heterosexual": "No responde",
    "A mi no me asignaron nada. Nací como la biología de mi madre se le ocurrió crearme.": "No responde",
    "Que clase de pregunta es esta, importa lo que uno es o lo que uno sabe, soy felizmente casado con una maravillosa mujer con 3 hijas hermosas.": "No responde",
    "Fiat uno": "No responde",
    "No vendan humo con este tipo de opciones, no se paren arriba de la naturaleza.": "No responde",
    "QUE ESTA MIERDA": "No responde",
    "no encuentro la clasificacion con la que me identifico, y no pienso usar la clasificacion que pretenden": "No responde",
    "Persona normal": "No responde",
    "Que te importa": "No responde",
    "No binarie": "Otro",
    "Ni idea, creia que era Hetero, pero bisexual me gusta mas": "Otro",
    "Genderqueer, y la pregunta anterior está mal redactada: o indican orientación o indican identidad de género (o separan en dos preguntas)": "Otro",
    "Agénero": "Otro",
    "Trans queer": "Otro",
    "Mujer Trans": "Otro",
    "Varón Trans": "Otro",
    "Mujer Pan": "Femenino",
    "Soy Varon": "Masculino",
    "macho alfa": "Masculino",
    "Varón Cis": "Masculino",
    "Femenino Trans": "Otro",
    "Hombre masculino": "Masculino",
    "hombre macho": "Masculino",
    "Masculino Trans": "Otro",
    "Macho Alfa": "Masculino",
    "Mujer Cis": "Femenino",
    "Mujer NB": "Femenino",
    "cactus": "No responde",
    "Enserio?": "No responde",
    "Bisexual": "No responde",
    "Travesti": "Otro",
    "Tester": "No responde",
    "Lesbiana": "No responde",
    "Normal": "No responde",
    "1": "No responde",
    "Oteo": "Otro",
    "cis": "Otro",
    "quetimporta": "No responde",
    "Humano": "No responde",
    "Mujer.": "Femenino",
    "hetero": "No responde",
    "Mujer": "Femenino",
    "Gay": "No responde",
    "Femenino ": "Femenino",
    "marica": "No responde",
    "Hola": "No responde",
    "Irrelevante": "No responde",
    "BI": "Otro",
    "Hombre???": "No responde",
    "FemeninoTrans": "Otro",
    "MACHO": "Masculino",
    "nene": "Masculino",
    "Hombre": "Masculino",
    "hombre": "Masculino",
    "Hombre ": "Masculino",
    "HOMBRE ": "Masculino",
    "HOMBRE": "Masculino",
    "Varón": "Masculino",
    "Varon": "Masculino",
    "varon": "Masculino",
    "poyi": "No responde",
    "Hetero": "No responde",
    "nan": "No responde",
    "Masculino ": "Masculino",
    "Varón ": "Masculino",
    ".": "No responde",
    "x": "No responde",
    "?": "Otro",
}
sysarmy_analysis.replace_str_in_col("genero", genders_to_replace)

# TODO: Move this to data_process
import pandas as pd
sysarmy_analysis.dataset["genero_num"] = pd.Categorical(sysarmy_analysis.dataset.genero).codes


# sysarmy_analysis.explore()
sysarmy_analysis.describe(graph=True)


# Handle zeros
col_fix_zeros = "sueldo_mensual_bruto_ars"
sysarmy_analysis.handle_zeros([col_fix_zeros], method="median")


# Handle missings
cols_check_missings = list(sysarmy_analysis.dataset.columns)

col_fix_missings = "guardias"
sysarmy_analysis.handle_missing([col_fix_missings], method="constant", constant="No")
cols_check_missings.remove(col_fix_missings)

col_fix_missings = "pandemia_percepcion"
sysarmy_analysis.handle_missing([col_fix_missings], method="median")
cols_check_missings.remove(col_fix_missings)

col_fix_missings = "sueldo_mensual_bruto_ars"
sysarmy_analysis.handle_missing([col_fix_missings], method="median")
cols_check_missings.remove(col_fix_missings)

cols_fix_missings = [
    "violencia_laboral",
    "max_nivel_estudios",
    "max_nivel_estudios_estado",
    "cursos_especializacion",
    "contribucion_open_source",
    "programacion_hobbie",
]
sysarmy_analysis.handle_missing([cols_fix_missings], method="constant", constant="No responde")
cols_check_missings = [i for i in cols_check_missings if i not in cols_fix_missings]

sysarmy_analysis.handle_missing(cols_check_missings, method="drop")


# Handle outliers
# Assume that a salary less than 10000 ARS is not possible (less than minimum wage)
# so it refers to a value in dollars
# TODO: does it worth to be in data_process.py?
col = "sueldo_mensual_bruto_ars"
sysarmy_analysis.dataset[col] = np.where(sysarmy_analysis.dataset[col] <= 10000, sysarmy_analysis.dataset[col] * USD_ARS, sysarmy_analysis.dataset[col])

cols_numeric.remove("personas_a_cargo") # The "outliers" here are real values so another method is used
sysarmy_analysis.handle_outliers(cols_numeric, method="drop_iqr")
sysarmy_analysis.handle_outliers(["personas_a_cargo"], method="drop_5_95")
cols_numeric.append("personas_a_cargo")

sysarmy_analysis.describe(graph=True)

            
# ----------------------------------------------------------------------------------
# Data processing
# ----------------------------------------------------------------------------------
all_cols_to_standard = cols_numeric

cols_to_standard = [
    "edad", 
    "experiencia_anios" ,
    "empresa_actual_anios",
    "personas_a_cargo",
    "sueldo_conformidad",
    # "sueldo_mensual_bruto_ars", 
    # "sueldo_ajuste_total_2021", 
    "recomendacion_laboral",
    "politicas_diversidad",
    "pandemia_percepcion",
]
sysarmy_analysis.standardize(cols_to_standard, "z_score")


# Bartlett test to know if PCA could be done
import scipy.stats as stats
stats.bartlett(*[sysarmy_analysis.dataset[col].tolist() for col in cols_to_standard])
# BartlettResult(statistic=774806.2025723966, pvalue=0.0)
# According to the pvalue (less than 0.05) we have enough evidence to reject the null
# hypotesis hence the variances is different among all the numeric (continuos) variables


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
# cols_numeric = ["PC1", "PC2"]

y = sysarmy_analysis.dataset[var_to_predict]
reg = LinearRegression()
reg.fit(xs[cols_numeric], y)
print("")
print("R2 coefficient: ")
print(reg.score(xs[cols_numeric], y))

# get importance
importances = reg.coef_
# summarize feature importance.
cols_importance = list(zip(cols_numeric, importances))
cols_importance_ordered = sorted(cols_importance, key=lambda x: x[1])

for col, importance in cols_importance_ordered:
	print(f"Feature: {col}, Score: {importance}")

# plot feature importance
plt.bar(list(zip(*cols_importance_ordered))[0], list(zip(*cols_importance_ordered))[1])
plt.xticks(rotation=90)
plt.show()


# ----------------------------------------------------------------------------------
# sysarmy_analysis.reset()
# print(sysarmy_analysis)

# sysarmy_analysis.save(output_path / "sysarmy_survey_analysed.csv")
# print(sysarmy_analysis)
