import logging
import os
from pathlib import Path

import numpy as np
from numpy.core.numeric import False_

import mappings as maps
from data_process import DataProcess

project_path = Path(os.getcwd())
output_path = project_path / "data/prepared/"
USD_ARS = 105

# ----------------------------------------------------------------------------------
# Data load
sysarmy_survey = project_path / "data/raw/2021.2 - sysarmy - Encuesta de remuneración salarial Argentina.csv"
sysarmy_analysis = DataProcess(sysarmy_survey, "csv", logging.INFO)


# ----------------------------------------------------------------------------------
# Data refine and exploration
# ----------------------------------------------------------------------------------
print(sysarmy_analysis)
# sysarmy_analysis.explore(name_postfix="raw_data")

sysarmy_analysis.drop_cols(maps.cols_to_drop)
print(sysarmy_analysis)

sysarmy_analysis.rename_cols(maps.cols_to_rename)

sysarmy_analysis.enforce_numeric(["sueldo_mensual_bruto_ars"])

print(sysarmy_analysis)
# sysarmy_analysis.describe(graph=True)

numeric_types = ["int8", "int16", "int32", "int64", "float8", "float16", "float32", "float64"]
cols_by_type = sysarmy_analysis.group_cols_by_type()
cols_numeric = sysarmy_analysis.get_cols_by_type(cols_by_type, numeric_types)


# Create technologies column unifying multiple related columns
sysarmy_analysis.unify_cols(maps.cols_to_unify, "technologies", maps.tecs_to_replace)
sysarmy_analysis.drop_cols(maps.cols_to_unify)


# Unify the multiple ways to refer to the gender, since the goal of this analysis is
# focus on the salary but not in diversity.
sysarmy_analysis.replace_str_in_col("genero", maps.genders_to_replace)


# Unify the values on the column "cursos_especializacion" due to contradictions in the categories
# if the response contains at least one "sí" then is an affirmative answer.
sysarmy_analysis.replace_str_in_col("cursos_especializacion", maps.courses_to_replace)

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
# Assume that a salary less than 10000 ARS is not possible (much less than the minimum wage in Argentina)
# so it refers to a value in dollars
# TODO: does it worth to be in data_process.py?
col = "sueldo_mensual_bruto_ars"
sysarmy_analysis.dataset[col] = np.where(sysarmy_analysis.dataset[col] <= 10000, sysarmy_analysis.dataset[col] * USD_ARS, sysarmy_analysis.dataset[col])

cols_numeric.remove("personas_a_cargo") # The "outliers" here are real values so another method is used
sysarmy_analysis.handle_outliers(cols_numeric, method="drop_iqr")
sysarmy_analysis.handle_outliers(["personas_a_cargo"], method="drop_5_95")
cols_numeric.append("personas_a_cargo")


# sysarmy_analysis.drop_cols(["technologies"])
# print(set(sysarmy_analysis.dataset))
# print(set(sysarmy_analysis.dataset[cols_to_standard]))
# print(set(sysarmy_analysis.dataset) - set(sysarmy_analysis.dataset[cols_to_standard]))
# sysarmy_analysis.drop_cols(list(set(sysarmy_analysis.dataset) - set(sysarmy_analysis.dataset[cols_to_standard])))
# print(list(sysarmy_analysis.dataset))
# sysarmy_analysis.explore(name_postfix="temp")


# Create dummy columns from categorical columns
sysarmy_analysis.dummy_cols_from_category(
    cols=["genero",
        "violencia_laboral",
        "tipo_contrato",
        "max_nivel_estudios",
        "cursos_especializacion",
        "guardias",
        "sueldo_bonos",
        "sueldo_ajuste_2021",
        "contribucion_open_source",
        "programacion_hobbie",
    ],
    drop_first=False,
)

sysarmy_analysis.describe(graph=True)
# sysarmy_analysis.explore(name_postfix="processed")

            
# ----------------------------------------------------------------------------------
# Data processing
# ----------------------------------------------------------------------------------
all_cols_to_standard = cols_numeric

cols_to_standard = [
    "edad", 
    "experiencia_anios" ,
    "empresa_actual_anios",
    "personas_a_cargo",
    # "sueldo_conformidad",
    # "sueldo_mensual_bruto_ars", 
    "sueldo_ajuste_total_2021", 
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
# hypothesis hence the variances is different among all the numeric (continuos) variables


# Dimensionality reduction using PCA:
# Applies only for numeric columns, requires standardized values
sysarmy_analysis.reduction_dims(
    cols_to_standard,
    method="pca",
    final_number_dims=2, 
    visualize=True
)

# Dimensionality reduction using MCA:
# Applies only for categoric columns
cols_by_type = sysarmy_analysis.group_cols_by_type()
cols_categoric = sysarmy_analysis.get_cols_by_type(cols_by_type, ["object"])
cols_categoric.remove("technologies") # This column is removed because it was manually created and it has a very high cardinality
sysarmy_analysis.reduction_dims(
    cols_categoric,
    method="mca",
    final_number_dims=5, 
    visualize=True
)

sysarmy_analysis.clusterization(
    cols_to_standard,
    method="dbscan", 
    visualize=True
)

sysarmy_analysis.dummy_cols_from_text(col="technologies", sep=",", n_cols=15)
print(sysarmy_analysis)


# Salary prediction with linear regression with cleaned columns, no dim reduction
# the method automatically select the numeric columns.
sysarmy_analysis.linear_regression(
    col_to_predict="sueldo_mensual_bruto_ars", 
    cols_to_remove=["PC1", "PC2", "MC1", "MC2", "MC3", "MC4", "MC5"], 
    graph=True,
)


# Salary prediction with random forest with cleaned columns, no dim reduction
sysarmy_analysis.random_forest(
    col_to_predict="sueldo_mensual_bruto_ars", 
    cols_to_remove=["technologies", "PC1", "PC2", "MC1", "MC2", "MC3", "MC4", "MC5"] + cols_categoric,
    graph=True,
)


# ----------------------------------------------------------------------------------
# sysarmy_analysis.reset()
# print(sysarmy_analysis)

# sysarmy_analysis.save(output_path / "sysarmy_survey_analysed.csv")
# print(sysarmy_analysis)
