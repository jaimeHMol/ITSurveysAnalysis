import logging
import os
from pathlib import Path

import numpy as np
from joblib import dump

import mappings as maps
from data_process import DataProcess

project_path = Path(os.getcwd())
output_path = project_path / "data/prepared/"
export_path = project_path / "export/"
USD_ARS = 105

# ----------------------------------------------------------------------------------
# Data load
# ----------------------------------------------------------------------------------
sysarmy_survey = (
    project_path
    / "data/raw/2021.2 - sysarmy - Encuesta de remuneración salarial Argentina.csv"
)
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

numeric_types = [
    "int8",
    "int16",
    "int32",
    "int64",
    "float8",
    "float16",
    "float32",
    "float64",
]
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
sysarmy_analysis.handle_missing(
    [cols_fix_missings], method="constant", constant="No responde"
)
cols_check_missings = [i for i in cols_check_missings if i not in cols_fix_missings]

sysarmy_analysis.handle_missing(cols_check_missings, method="drop")


# Handle outliers
# Assume that a salary less than 10000 ARS is not possible (much less than the minimum wage in Argentina)
# so it refers to a value in dollars
col = "sueldo_mensual_bruto_ars"
sysarmy_analysis.dataset[col] = np.where(
    sysarmy_analysis.dataset[col] <= 10000,
    sysarmy_analysis.dataset[col] * USD_ARS,
    sysarmy_analysis.dataset[col],
)

cols_numeric.remove(
    "personas_a_cargo"
)  # The "outliers" here are real values so another method is used
sysarmy_analysis.handle_outliers(cols_numeric, method="drop_iqr")
sysarmy_analysis.handle_outliers(["personas_a_cargo"], method="drop_5_95")
cols_numeric.append("personas_a_cargo")

# Create dummy columns from categorical columns
sysarmy_analysis.dummy_cols_from_category(
    cols=[
        "genero",
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
    # "sueldo_mensual_bruto_ars",
    "sueldo_ajuste_total_2021",
    "experiencia_anios",
    "empresa_actual_anios",
    "personas_a_cargo",
    "recomendacion_laboral",
    "politicas_diversidad",
    "edad",
    # "sueldo_conformidad",
    # "pandemia_percepcion",
]

scaler_X = sysarmy_analysis.standardize(cols_to_standard, "z_score")
scaler_y = sysarmy_analysis.standardize(["sueldo_mensual_bruto_ars"], "z_score")

# Bartlett test to know if PCA could be done
import scipy.stats as stats

stats.bartlett(*[sysarmy_analysis.dataset[col].tolist() for col in cols_to_standard])
# BartlettResult(statistic=774806.2025723966, pvalue=0.0)
# According to the pvalue (less than 0.05) we have enough evidence to reject the null
# hypothesis hence the variances is different among all the numeric (continuos) variables

# Dimensionality reduction using PCA:
# Applies only for numeric columns, requires standardized values
sysarmy_analysis.reduction_dims(
    cols_to_standard, method="pca", final_number_dims=2, visualize=True
)

# Dimensionality reduction using MCA:
# Applies only for categoric columns
cols_by_type = sysarmy_analysis.group_cols_by_type()
cols_categoric = sysarmy_analysis.get_cols_by_type(cols_by_type, ["object"])
# This column is removed because it was manually created and it has a very high cardinality
cols_categoric.remove("technologies")
sysarmy_analysis.reduction_dims(
    cols_categoric, method="mca", final_number_dims=5, visualize=True
)

sysarmy_analysis.clusterization(cols_to_standard, method="dbscan", visualize=True)

sysarmy_analysis.dummy_cols_from_text(col="technologies", sep=",", n_cols=15)


# ----------------------------------------------------------------------------------
# Data modelling
# ----------------------------------------------------------------------------------
linear_regression_ridge, cv_lrr_models  = sysarmy_analysis.linear_regression_ridge(
    col_to_predict="sueldo_mensual_bruto_ars",
    cols_to_remove=["technologies", "PC1", "PC2", "MC1", "MC2", "MC3", "MC4", "MC5"]
    + cols_categoric,
    # cols=["PC1", "PC2", "MC1", "MC2", "MC3", "MC4", "MC5"],
    graph=True,
    num_vars_graph=15,
)

# Salary prediction using random forest with cleaned columns.
random_forest, cv_rf_models = sysarmy_analysis.random_forest(
    col_to_predict="sueldo_mensual_bruto_ars",
    cols_to_remove=["technologies", "PC1", "PC2", "MC1", "MC2", "MC3", "MC4", "MC5"]
    + cols_categoric,
    # cols=["PC1", "PC2", "MC1", "MC2", "MC3", "MC4", "MC5"],
    graph=True,
    num_vars_graph=15,
)


# -----------------------------------------------------------------------------------
# Common variables on the top 15 more important between the two models (66 total number of variables).
# -----------------------------------------------------------------------------------
common_vars_dict = {}
top_vars_linear_regression_ridge = dict(linear_regression_ridge.top_vars_graph)
top_vars_random_forest = dict(random_forest.top_vars_graph)
common_vars_set = set(top_vars_linear_regression_ridge) & set(top_vars_random_forest)
for var in common_vars_set:
    # common_vars_dict[var] = (list(top_vars_linear_regression_ridge).index(var), list(top_vars_random_forest).index(var))
    common_vars_dict[var] = list(top_vars_linear_regression_ridge).index(var) + list(top_vars_random_forest).index(var)
print(f"The common top more important variables between the two models are: {common_vars_dict}")

# Predict using the data from the row zero just for testing purposes
all_cols = list(sysarmy_analysis.dataset)
cols_to_remove = ["sueldo_mensual_bruto_ars", "technologies", "PC1", "PC2", "MC1", "MC2", "MC3", "MC4", "MC5"] + cols_categoric
for col in cols_to_remove:
    all_cols.remove(col) 
row_to_predict = 1
X_to_predict = list(sysarmy_analysis.dataset[all_cols].iloc[row_to_predict])
y_real = sysarmy_analysis.dataset["sueldo_mensual_bruto_ars"].iloc[row_to_predict]
y_predict_rf = random_forest.predict([X_to_predict])
y_predict_lrr = linear_regression_ridge.predict([X_to_predict])
{"y_real": y_real, "y_predict_rf": y_predict_rf, "y_predict_lrr": y_predict_lrr}
scaler_y.inverse_transform([y_real, y_predict_rf, y_predict_lrr])


# Export the best models
dump(linear_regression_ridge, export_path / "export_linear_regression_ridge.joblib")
dump(random_forest, export_path / "export_random_forest.joblib")
dump(scaler_y, export_path / "export_scaler_output.joblib")
dump(scaler_X, export_path / "export_scaler_input.joblib")

# ----------------------------------------------------------------------------------
# sysarmy_analysis.reset()
# print(sysarmy_analysis)

# sysarmy_analysis.save(output_path / "sysarmy_survey_analysed.csv")
# print(sysarmy_analysis)
