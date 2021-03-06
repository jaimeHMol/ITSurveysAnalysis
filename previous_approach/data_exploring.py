# -------------------------------------------------------------------------------------------------------------------
# Template script for a data science analysis
# Sep 2020
# @jaimehmol
# -------------------------------------------------------------------------------------------------------------------


# ---------------
# Start date time
# ---------------


# ---------------
# Imports general
# ---------------
import pandas as pd
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from kneed import KneeLocator

from data_process import DataProcess
# import warnings
# warnings.filterwarnings('ignore')
# %matplotlib inline


# --------------
# Imports owned
# --------------


# ------------------------------
# Global variables and constants
# ------------------------------
project_path         =  Path(os.getcwd())
script               =  "data_exploring.py"
prob_training        =  0.7
prob_testing         =  1 - prob_training
seed                 =  777677 # Random seed

# TODO: Mejor la asignación de los nombres y rutas a utilizar
sysarmy_survey       =  project_path / "data/raw/2020.2 - sysarmy - Encuesta de remuneración salarial Argentina.csv"
stackoverflow_survey =  project_path / "data/raw/survey_results_public.csv"
output_file          =  ""
aux_file             =  ""
separator            =  "|" #" "  ";"  "," 
decimal              =  "."             
campo_id             =  "" #(identificador único de cada fila)
campos_a_borrar      =  [] #Variables (columnas) a borrar


# -------------
# Global setup
# -------------


# -----------------------
# Loading source datasets
# -----------------------

# MANUAL INPUT.
# invoices = {'invoice': [1, 2, 3, 4, 5, 6],
#             'client': [4, 1, 3, 1, 2, 6],
#             'units': [3, 2, 1, 2, 1, 1],
#             'price': [27.76, 21.13, 29.82, 29.96, 21.11, 23.97],
#             'total': [83.28, 42.26, 29.82, 59.92, 21.11, 23.97]}
# dfSource = pd.DataFrame(invoices)

# FROM THE WEB. Requieres internet access

# CSV.
dfSourceSysArmy = pd.read_csv(sysarmy_survey)
sysarmy_analysis = DataProcess(sysarmy_survey, 'csv')
print(sysarmy_analysis)

dfSourceStackOverflow = pd.read_csv(stackoverflow_survey)

# TEXT FLAT FILE.


# EXCEL.
 

# ===================================================================================================================
# Data explorations (Columns)
# ===================================================================================================================


# SYSARMY SURVEY
# --------------
# Quantitative description  of the input dataset and its variables
# ----------------------------------------------------------------
for col in dfSourceSysArmy.columns:
  print("="*27)
  print(col)
  print("="*27)
  print(dfSourceSysArmy[col].describe())
  print("")

dfSourceSysArmy.describe(include="all")

# Graphic description of the variables
# ------------------------------------
# Histogram
sns.distplot(dfSourceSysArmy["Salario mensual BRUTO (en tu moneda local)"])

# Scatter plot
var = "Años de experiencia"
data = pd.concat([dfSourceSysArmy["Salario mensual BRUTO (en tu moneda local)"], dfSourceSysArmy[var]], axis=1)
data.plot.scatter(x=var, y="Salario mensual BRUTO (en tu moneda local)", ylim=(0,800000))

# Box plot 
var = "Años de experiencia"
data = pd.concat([dfSourceSysArmy["Salario mensual BRUTO (en tu moneda local)"], dfSourceSysArmy[var]], axis=1)
f, ax = plt.subplots(figsize=(8, 6))
fig = sns.boxplot(x=var, y="Salario mensual BRUTO (en tu moneda local)", data=data)
fig.axis(ymin=0, ymax=800000)

# TOFIX
var = "Me identifico"
data = pd.concat([dfSourceSysArmy["Salario mensual BRUTO (en tu moneda local)"], dfSourceSysArmy[var]], axis=1)
f, ax = plt.subplots(figsize=(8, 6))
fig = sns.boxplot(x=var, y="Me identifico", data=data)
fig.axis(ymin=0, ymax=800000)

# Correlation matrix
corrmat = dfSourceSysArmy.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True)

# Matrix scatterplot
sns.set()
cols = ["Salario mensual BRUTO (en tu moneda local)", 
  "Años de experiencia", "Años en la empresa actual", 
  "Tengo", "Cantidad de empleados", 
  "¿La recomendás como un buen lugar para trabajar?"]
sns.pairplot(dfSourceSysArmy[cols], size = 2.5)
plt.show()


# TODO: Removing unsed columns
# ----------------------------
cols_to_remove = [
    'Estoy trabajando en',
    'Años en el puesto actual',
    'Cuánto cobrás por guardia',
    '¿Porcentaje, bruto o neto?',                  
    'Salario mensual NETO (en tu moneda local)',
    'Cómo creés que está tu sueldo con respecto al último semestre',
    'A qué está atado el bono',
    '¿Tenés algún tipo de discapacidad?',
    '¿Sentís que esto te dificultó el conseguir trabajo?',
    '¿En qué mes fue el último ajuste?',
    'Beneficios extra',   
    '¿Cuáles considerás que son las mejores empresas de IT para trabajar en este momento, en tu ciudad?',
]
sysarmy_analysis.remove_cols(cols_to_remove)


# TODO: Renaming columns
# ----------------------------
cols_to_rename = {
    'Me identifico': 'genero',
    'Tengo': 'edad',
    'Dónde estás trabajando': 'ubicacion',
    'Nivel de estudios alcanzado': 'max_nivel_estudios',
    'Estado': 'max_nivel_estudios_estado',
    'Realizaste cursos de especialización': 'cursos_especializacion',
    '¿Contribuís a proyectos open source?': 'contribucion_open_source',
    '¿Programás como hobbie?': 'programacion_hobbie',
    'Trabajo de': 'rol_trabajo',
    '¿Qué SO usás en tu laptop/PC para trabajar?': 'computador_trabajo_so',
    '¿Y en tu celular?': 'celular_so',
    '¿Tenés guardias?': 'guardias',
    'Salario mensual BRUTO (en tu moneda local)': 'sueldo_mensual_bruto_ars',
    'Sueldo dolarizado?': 'sueldo_dolarizado',
    '¿Qué tan conforme estás con tu sueldo?': 'sueldo_conformidad',
    'Recibís algún tipo de bono': 'sueldo_bonos',
    '¿Tuviste ajustes por inflación en lo que va de 2020?': 'sueldo_ajustes_inflacion',
    '¿De qué % fue el ajuste total?': 'sueldo_ajuste_total_2020',
    '¿Sufriste o presenciaste situaciones de violencia laboral?': 'violencia_laboral',
    '¿La recomendás como un buen lugar para trabajar?': 'recomendacion_laboral',
    '¿Cómo calificás las políticas de diversidad e inclusión?': 'politicas_diversidad',
}

sysarmy_analysis.rename_cols(cols_to_rename)





# STACKOVERFLOW SURVEY
# --------------------
# Quantitative description  of the input dataset and its variables
# ----------------------------------------------------------------
for col in dfSourceStackOverflow.columns:
  print("="*27)
  print(col)
  print("="*27)
  print(dfSourceStackOverflow[col].describe())
  print("")


# Graphic description of the variables
# ------------------------------------
# Histogram
sns.distplot(dfSourceStackOverflow["ConvertedComp"])

# TOFIX
# Scatter plot
var = "YearsCodePro"
data = pd.concat([dfSourceStackOverflow["ConvertedComp"], dfSourceStackOverflow[var]], axis=1)
data.plot.scatter(x=var, y="ConvertedComp", ylim=(0,800000))

# Box plot 
var = "YearsCodePro"
data = pd.concat([dfSourceStackOverflow["ConvertedComp"], dfSourceStackOverflow[var]], axis=1)
f, ax = plt.subplots(figsize=(8, 6))
fig = sns.boxplot(x=var, y="ConvertedComp", data=data)
fig.axis(ymin=0, ymax=800000)

# TOFIX
var = "Gender"
data = pd.concat([dfSourceStackOverflow["ConvertedComp"], dfSourceStackOverflow[var]], axis=1)
f, ax = plt.subplots(figsize=(8, 6))
fig = sns.boxplot(x=var, y="Gender", data=data)
fig.axis(ymin=0, ymax=800000)

# Correlation matrix
corrmat = dfSourceStackOverflow.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True)

# Matrix scatterplot
sns.set()
cols = ["ConvertedComp", 
  "YearsCodePro", 
  "Age", "OrgSize", 
  "JobSat"]
sns.pairplot(dfSourceStackOverflow[cols], size = 2.5)
plt.show()



# ---------------------
# Outliers analysis
# ---------------------


# Removing salary values to much high (in the field CompTotal)
# Selecting the rows with outliers (values 20 times bigger than the third quartile of the
# values distribution of the dataset)
dfSourceStackOverflow.loc[dfSourceStackOverflow['CompTotal'] > 30000000]

# Index to delete
rowsToRemove = dfSourceStackOverflow.loc[dfSourceStackOverflow['CompTotal'] > 30000000].index
dfSourceStackOverflow = dfSourceStackOverflow.drop(rowsToRemove, axis=0)


# -------------------------------------------------------------
# Distribution analysis (Normality, homoscedasticity, etc)
# -------------------------------------------------------------




# ===================================================================================================================
# Data qualty and cleaning (columns)
# ===================================================================================================================

# ----------------------------------------
# Missing values (Missings, NA, Nulls)
# ----------------------------------------
# SysArmy
total = dfSourceSysArmy.isnull().sum().sort_values(ascending=False)
percent = (dfSourceSysArmy.isnull().sum()/dfSourceSysArmy.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)


# StackOverflow
# Quitar filas con valores faltantes
dfSourceStackOverflow = dfSourceStackOverflow.dropna(axis=0)

# Chosing features (variables) to work
features = ['WorkWeekHrs', 'ConvertedComp', 'Age', 'Respondent']
# Separating out the features
x = dfSourceStackOverflow.loc[:, features].values
y = dfSourceStackOverflow.loc[:, features]
# Separating out the target
# y = dfSourceStackOverflow.loc[:,['target']].values

# Standardizing the values using z-score
standardized_features = StandardScaler().fit_transform(y)
# TODO: Try standardizing the values transforming to 0 to 1 scale


# JetBrains



# --------------------------------------------------------------------
# Dimensionality analys and reduction (PCA) - StackOverflow Survey
# --------------------------------------------------------------------
# PCA is affected by scale so we will use the standardized values
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(standardized_features)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

pca.explained_variance_ratio_ # BAD!

# Visualizar PCA
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
# targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
# colors = ['r', 'g', 'b']
# for target, color in zip(targets,colors):
    # indicesToKeep = principalDf['target'] == target
ax.scatter(principalDf['principal component 1']
            , principalDf['principal component 2']
            , s = 50)
# ax.legend(targets)
ax.grid()




# -----------------------------------------------------------------------------------------------------
# Data transformation (Format, conversions, adjustments, replaces, dummy variables, regular expresions)
# -----------------------------------------------------------------------------------------------------
# Convert categorical variable into dummy
# dfSource = pd.get_dummies(dfSource)



# ===================================================================================================================
# Integration, agregation and enrichment
# ===================================================================================================================



# ===================================================================================================================
# Modeling
# ===================================================================================================================

# Clustering - Kmeans (initial approach with 3 clusters)
kmeans = KMeans(
    init="random",
    n_clusters=3,
    n_init=10,
    max_iter=300,
    random_state=42,
)
kmeans.fit(standardized_features)

# The lowest Sum of Squared Error (SSE) value
kmeans.inertia_

# Final locations of the centroid
kmeans.cluster_centers_

# The number of iterations required to converge
kmeans.n_iter_

# How many clusters should be calculated?
#   Using elbow method
print("="*27)
print("Clustering using K-Means")
print("="*27)
kmeans_kwargs  = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}

sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(standardized_features)
    sse.append(kmeans.inertia_)

plt.style.use("fivethirtyeight")
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.title("K-Means")
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )
# Best number of clusters:
number_clusters_best = kl.elbow
print(f"Best number of clusters using elbow method: {number_clusters_best}")

# Silhouette coefficient (goes from -1 to 1, near to 1 is better)
kmeans_silhouette_coefficients = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(standardized_features)
    score = silhouette_score(standardized_features, kmeans.labels_)
    kmeans_silhouette_coefficients.append(score)

plt.style.use("fivethirtyeight")
plt.plot(range(2, 11), kmeans_silhouette_coefficients)
plt.xticks(range(2, 11))
plt.title("K-Means")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Coefficient")
plt.show()



# Clustering - Kmedoids (initial approach with 3 clusters)
kmedoids = KMedoids(
    metric="euclidean",
    n_clusters=3,
)
kmedoids.fit(standardized_features)

# The lowest Sum of Squared Error (SSE) value
kmedoids.inertia_

# Final locations of the centroid
kmedoids.cluster_centers_

# The number of iterations required to converge
kmedoids.n_iter_

# How many clusters should be calculated?
#   Using elbow method
print("="*27)
print("Clustering using K-Medoids")
print("="*27)

kmedoids_kwargs  = {
    "metric": "euclidean",
}

sse = []
for k in range(1, 11):
    kmedoids = KMedoids(n_clusters=k, **kmedoids_kwargs)
    kmedoids.fit(standardized_features)
    sse.append(kmedoids.inertia_)

plt.style.use("fivethirtyeight")
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.title("K-Medoids")
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )
# Best number of clusters:
number_clusters_best = kl.elbow
print(f"Best number of clusters using elbow method: {number_clusters_best}")

# Silhouette coefficient (goes from -1 to 1, near to 1 is better)
kmedoids_silhouette_coefficients = []
for k in range(2, 11):
    kmedoids = KMedoids(n_clusters=k, **kmedoids_kwargs)
    kmedoids.fit(standardized_features)
    score = silhouette_score(standardized_features, kmedoids.labels_)
    kmedoids_silhouette_coefficients.append(score)

plt.style.use("fivethirtyeight")
plt.plot(range(2, 11), kmedoids_silhouette_coefficients)
plt.xticks(range(2, 11))
plt.title("K-Medoids")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Coefficient")
plt.show()



# Clustering - DBScan
print("="*27)
print("Clustering using DBScan")
print("="*27)
dbscan = DBSCAN(eps=0.5)

dbscan.fit(standardized_features)

# Number of clusters (For the eps used as input parameter)
len(set(dbscan.labels_))

dbscan_silhouette = silhouette_score(standardized_features, dbscan.labels_)

# Finding best number of cluster (Choosing the correct eps)
dbscan_silhouette_coefficients = []
for eps in np.linspace(0.1,4,10):
    dbscan = DBSCAN(eps=eps)
    dbscan.fit(standardized_features)
    score = silhouette_score(standardized_features, dbscan.labels_)
    dbscan_silhouette_coefficients.append(score)

plt.style.use("fivethirtyeight")
plt.plot(np.linspace(0.1,4,10), dbscan_silhouette_coefficients)
plt.xticks(np.linspace(0.1,4,10))
plt.title("DBScan")
plt.xlabel("eps")
plt.ylabel("Silhouette Coefficient")
plt.show()

# TODO: Detect this value programatically
dbscan = DBSCAN(eps=1.8)
dbscan.fit(standardized_features)

# Best number of clusters according to the best Silhouette score over multiples eps.
number_clusters_best = len(set(dbscan.labels_))
print(f"Best number of clusters using Silhouette over multiple eps: {number_clusters_best}")




# ----------------------------------------------------------------------------
# Building data model validation structure (Train-Test, CrossValidation, etc.)
# ----------------------------------------------------------------------------
from sklearn.model_selection import train_test_split
# test_size: what proportion of original data is used for test set
train_img, test_img, train_lbl, test_lbl = train_test_split( mnist.data, mnist.target, test_size=1/7.0, random_state=0)



# ------------------------------------
# Build, train and test the data model
# ------------------------------------


linea = linea + 1











# ----------------------
# Evaluation and results
# ----------------------
# TODO: 
# Llamar a función propia que haga 
#   1. Métricas de los resultados
#     1.1. Tabla de confusión
#     1.2. Área bajo la curva ROC
#     1.3. Accuracy
#   2. Gráficas de resultados
#     2.1. Curvas ROC
# Entrada: Data frame con dataset de Test (inicial)
#          Objeto con el modelo a aplicar (con sus respectivos parámetros) 
# Salida: Data frame con resultados ordenados
#         Gráficos



# ===================================================================================================================
# Ending
# ===================================================================================================================

# ---------------------------------
# Total execution time calculation  
# ---------------------------------


# ===================================================================================================================
# Local functions
# ===================================================================================================================


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                 A P E N D I C E            (Descomentar lo que se requiera ctr + shift + C)
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------
# # Aplicación de tests
# # -------------------------------------------------------------------------------------------------------------------
# # ******************************** UNIVARIADO DOS MUESTRAS ***************************************
# # Test de normalidad de Kolmogorov-Smirnof
# lillie.test(ejerc1DF$tpos1)
# # Evaluar el valor p y comparar con alfa
# lillie.test(ejerc1DF$tpos2)
# # Evaluar el valor p y comparar con alfa
# 
# # Box-cox para buscar exponente de transformación a distribución normal en caso de que no la tengan
# boxcoxTpos1 <- boxcox(ejerc1DF$tpos1~1,plotit=T)
# boxcoxTpos2 <- boxcox(ejerc1DF$tpos2~1,plotit=T)
# # Busqueda del exponente para transformar a normal
# exponenteTpos1 <- boxcoxTpos1$x[which(boxcoxTpos1$y == max(boxcoxTpos1$y))]
# exponenteTpos2 <- boxcoxTpos2$x[which(boxcoxTpos2$y == max(boxcoxTpos2$y))]
# # Aplica transformación con exponenete a hallado en box cox
# tpos1Transf <- ejerc1DF$tpos1^(exponenteTpos1)
# tpos2Transf <- ejerc1DF$tpos2^(exponenteTpos2)
# 
# # ---------------------------------------------------------.
# # Boxcox de ambas muestras al mismo tiempo (Opcional)
# attach(ejerc1DF)
# casos <- c(tpos1,tpos2)
# tpos <- c(rep(c("tpos1","tpos2"), each =20))
# test <- boxcox(casos~1,plotit=T)
# exponenteTposAll <- test$x[which(test$y == max(test$y))]
# # ---------------------------------------------------------.
# 
# # Test de normalidad a los datos transformados
# lillie.test(tpos1Transf)
# # Evaluar el valor p y comparar con alfa
# lillie.test(tpos2Transf)
# # Evaluar el valor p y comparar con alfa
# 
# # Test t de diferencia de medias paramétrico
# testT <- t.test(tpos1Transf,tpos2Transf)
# print(testT)
# # Evaluar el valor p y comparar con alfa
# 
# # Test de diferencia de medias NO paramétrico: Wilcoxon - Man - Whitney
# wilcox.test(ejerc1DF$tpos1,ejerc1DF$tpos2)
# # Evaluar el valor p y comparar con alfa. Si estamos seguros que las dos muestras tienen la misma distribución
# # denota diferencia de las medianas (posicional), si no estamos seguros sobre la igualdad de distribución
# # solo denota que las distribuciones son diferentes
# 
# 
# 
# # ******************************** UNIVARIADO MÁS DE DOS MUESTRAS ********************************
# 
# # Exploración inicial (gráfica y numérica) de datos
# # --------------------------------------------------------------.  
# boxplot(dfSource[,])
# boxplotInfo <- boxplot(dfSource[,])
# boxplotInfo
# stat.desc(dfSource[,]) 
# 
# 
# # Aplicación de anova multivariado
# # --------------------------------------------------------------.
# attach(dfSource)
# casos <- c(An1,An2,An3,An4)
# 
# grupos <- c(rep(c("An1","An2","An3","An4"), each =3))
# 
# anovaS = aov(casos ~ grupos)
# summary(anovaS)
# residuos <- residuals(anovaS)
# # Evaluar el valor p y comparar con alfa
# 
# 
# # Verificación de supuestos 
# # --------------------------------------------------------------.
# # Normalidad
# 
# shapiro.test(An1)
# shapiro.test(An2)
# shapiro.test(An3)
# shapiro.test(An4)
# shapiro.test(residuos) #Sobre los residuos para no tener que hacer el test de shapiro para cada muestra
# # Evaluar el valor p y comparar con alfa
# 
# # NO APLICA, TAMAÑO DE MUESTRAS MUY PEQUEÑO
# lillie.test(An1)
# lillie.test(An2)
# lillie.test(An3)
# lillie.test(An4)
# lillie.test(residuos) #Sobre los residuos para no tener que hacer el test de shapiro para cada muestra
# # Evaluar el valor p y comparar con alfa
# 
# # NO APLICA, TAMAÑO DE MUESTRAS MUY PEQUEÑO
# agostino.test(An1)
# agostino.test(An2)
# agostino.test(An3)
# agostino.test(An4)
# agostino.test(residuos)
# # Evaluar el valor p y comparar con alfa
# 
# 
# # Homocedasticidad
# #marcasFactor <- as.factor(marcas)
# levene.test(casos~grupos)
# # Evaluar el valor p y comparar con alfa
# bartlett.test(casos~grupos)
# # Evaluar el valor p y comparar con alfa
# 
# # En caso de cumplir supuestos y tener un ANOVA que denote que hay diferencias en las medias, se puede 
# # buscar cuales son las muestras que presentan medias diferentes con Tukey. Usar el mismo nivel de confianza
# # usado para el ANOVA
# TukeyHSD(anovaMarcas, conf.level = 0.95)
# # Evaluar el valor p y comparar con alfa en los casos donde el rango inferior y superior contenga el cero
# # esto nos indicará que el par de muestras tienen media similar
# 
# # NO USAR MODELO PARAMÉTRICO, SI LA MUESTRA ES MUY PEQUEÑA
# 
# 
# 
# # Analisis de la varianza multivariado no paramétrico (KRUSKAL WALLIS)
# # --------------------------------------------------------------------.
# gruposFact <- as.factor(grupos) #OJO: para este test se requiere que la variable de clasificación sea tipo factor
# kruskal.test(casos ~ gruposFact)
# # Evaluar el valor p y comparar con alfa
# -----------------------------------------------------------------------
