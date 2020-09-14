# -------------------------------------------------------------------------------------------------------------------
# Template Script Data Mining
# -------------------------------------------------------------------------------------------------------------------
# Plantilla con la estructura principal para un script en R para an�lisis de data mining / data science
# Sep 2020
# @jaimehmol
# -------------------------------------------------------------------------------------------------------------------

# ===================================================================================================================
# Inicio
# ===================================================================================================================

# -------------------------
# Almacena tiempo de inicio
# -------------------------


# ------------------
# Imports
# ------------------
import

# -------------------------
# Imports propios
# -------------------------
import

# -------------------
# Constantes globales
# -------------------
script             =  "data_exploring.py"
algoritmo            =  ""
busqueda             =  "" # B�squeda hiperpar�metros
estimacion           =  "" # Estimaci�n de rendimiento del modelo clasificador
prob_training        =  0.7
prob_testing         =  1 - prob_training
semilla              =  777677 # Para generaci�n de aleatoriedad

# TODO: Mejor la asignaci�n de los nombres y rutas a utilizar
archivo_entrada      =  ""
archivo_salida       =  ""
archivo_auxiliar     =  ""
separador            =  "|" #" "  ";"  "," 
decimal              =  "."             
campo_id             =  "" #(identificador �nico de cada fila)
campos_a_borrar      =  [] #Variables (columnas) a borrar


# ------------------------
# Configuraciones globales
# ------------------------
# -- WORKING DIRECTORY
#setwd("R:\\") # Mi directorio de trabajo
#setwd('M:\\') # o apuntando a una unidad virtual creada (ideal para manejar rutas relativas)

# -- HOME DIRECTORY
#Sys.setenv(R_USER="R:\\")


# -------------------
# Cargar datos fuente
# -------------------

# DESDE LA WEB. Requiere acceso a internet
#dfSource <- read.csv("http://astrostatistics.psu.edu/datasets/COMBO17.csv", header=T, stringsAsFactors=F)

# CSV que tiene cada muestra como  una columna
#dfSource <- data.frame(read.csv2(file=archivo_entrada, sep=separador,  dec=decimal,  stringsAsFactors=FALSE))

# ARCHIVO PLANO en general # HINT: Con algunos files me ha fallado
# dfSource <- read.table(archivo_entrada, sep=separador, dec=decimal, header=TRUE)

# EXCEL que tiene cada muestra como  una columna
#dfSource <- read_excel(path=archivo_entrada, sheet=1)  


# ===================================================================================================================
# Exploraci�n de variables (columnas)
# ===================================================================================================================

# ----------------------------------------------------------------
# Descripci�n cuantitativa del data set de entrada y sus variables
# ----------------------------------------------------------------


# --------------------------------
# Descripci�n gr�fica de variables
# --------------------------------


# ---------------------
# An�lisis de Outliers
# ---------------------


# -------------------------------------------------------------
# An�lisis de distribuci�n (Normalidad, Homocedasticidad, etc)
# -------------------------------------------------------------




# ===================================================================================================================
# Calidad y limpieza de variables (columnas)
# ===================================================================================================================

# ----------------------------------------
# Valores faltantes (Missings, NA, Nulos)
# ----------------------------------------



# ------------------------------------------------------------------------------------------------
# Transformaciones de datos (Formateos, Conversiones, Ajustes, Reemplazos, Expresiones Regulares)
# ------------------------------------------------------------------------------------------------



# ===================================================================================================================
# Integraci�n, agregaci�n y enriquecimiento
# ===================================================================================================================



# ===================================================================================================================
# Modelado
# ===================================================================================================================

# ---------------------------------------------------------------------------
# Construcci�n metodolog�a de validaci�n (Train-Test, CrossValidation, etc.)
# ---------------------------------------------------------------------------



# --------------------------------------------------------------------------
# B�squeda de hiperpar�metros (par�metros �ptimos) del modelo a implementar
# --------------------------------------------------------------------------

# Escribir el encabezado del archivo de salida
if( !file.exists(archivo_salida) )
{
  cat( "Id ejecuci�n", 
       "tiempo_promedio",
       "parametro1", 
       "parametro2",
       "fecha", 
       "dataset", 
       "clase", 
       "programa", 
       "algoritmo", 
       "busqueda" , 
       "estimacion",
       "\n", sep="\t", file=archivo_salida, fill=FALSE, append=FALSE )
}
lineas_archivo <-  length( readLines(archivo_salida) )  - 1
linea <- 1



# Proceso de escritura de archivo de salida



# ----------------------------------------
# Construcci�n y entrenamiento del modelo
# ----------------------------------------
# Ejecuci�n


linea = linea + 1


# Fin ejecuciones




# ------------------------
# Resultados y evaluaci�n
# ------------------------
# TODO: 
# Llamar a funci�n propia que haga 
#   1. M�tricas de los resultados
#     1.1. Tabla de confusi�n
#     1.2. �rea bajo la curva ROC
#     1.3. Accuracy
#   2. Gr�ficas de resultados
#     2.1. Curvas ROC
# Entrada: Data frame con dataset de Test (inicial)
#          Objeto con el modelo a aplicar (con sus respectivos par�metros) 
# Salida: Data frame con resultados ordenados
#         Gr�ficos



# ===================================================================================================================
# Finalizaci�n
# ===================================================================================================================

# ------------------------------
# C�lculo de tiempo de ejecuci�n 
# ------------------------------


# ===================================================================================================================
# Funciones locales
# ===================================================================================================================


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                 A P E N D I C E            (Descomentar lo que se requiera ctr + shift + C)
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------
# # Aplicaci�n de tests
# # -------------------------------------------------------------------------------------------------------------------
# # ******************************** UNIVARIADO DOS MUESTRAS ***************************************
# # Test de normalidad de Kolmogorov-Smirnof
# lillie.test(ejerc1DF$tpos1)
# # Evaluar el valor p y comparar con alfa
# lillie.test(ejerc1DF$tpos2)
# # Evaluar el valor p y comparar con alfa
# 
# # Box-cox para buscar exponente de transformaci�n a distribuci�n normal en caso de que no la tengan
# boxcoxTpos1 <- boxcox(ejerc1DF$tpos1~1,plotit=T)
# boxcoxTpos2 <- boxcox(ejerc1DF$tpos2~1,plotit=T)
# # Busqueda del exponente para transformar a normal
# exponenteTpos1 <- boxcoxTpos1$x[which(boxcoxTpos1$y == max(boxcoxTpos1$y))]
# exponenteTpos2 <- boxcoxTpos2$x[which(boxcoxTpos2$y == max(boxcoxTpos2$y))]
# # Aplica transformaci�n con exponenete a hallado en box cox
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
# # Test t de diferencia de medias param�trico
# testT <- t.test(tpos1Transf,tpos2Transf)
# print(testT)
# # Evaluar el valor p y comparar con alfa
# 
# # Test de diferencia de medias NO param�trico: Wilcoxon - Man - Whitney
# wilcox.test(ejerc1DF$tpos1,ejerc1DF$tpos2)
# # Evaluar el valor p y comparar con alfa. Si estamos seguros que las dos muestras tienen la misma distribuci�n
# # denota diferencia de las medianas (posicional), si no estamos seguros sobre la igualdad de distribuci�n
# # solo denota que las distribuciones son diferentes
# 
# 
# 
# # ******************************** UNIVARIADO M�S DE DOS MUESTRAS ********************************
# 
# # Exploraci�n inicial (gr�fica y num�rica) de datos
# # --------------------------------------------------------------.  
# boxplot(dfSource[,])
# boxplotInfo <- boxplot(dfSource[,])
# boxplotInfo
# stat.desc(dfSource[,]) 
# 
# 
# # Aplicaci�n de anova multivariado
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
# # Verificaci�n de supuestos 
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
# # NO APLICA, TAMA�O DE MUESTRAS MUY PEQUE�O
# lillie.test(An1)
# lillie.test(An2)
# lillie.test(An3)
# lillie.test(An4)
# lillie.test(residuos) #Sobre los residuos para no tener que hacer el test de shapiro para cada muestra
# # Evaluar el valor p y comparar con alfa
# 
# # NO APLICA, TAMA�O DE MUESTRAS MUY PEQUE�O
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
# # esto nos indicar�a que el par de muestras tienen media similar
# 
# # NO USAR MODELO PARAM�TRICO, SI LA MUESTRA ES MUY PEQUE�A
# 
# 
# 
# # Analisis de la varianza multivariado no param�trico (KRUSKAL WALLIS)
# # --------------------------------------------------------------------.
# gruposFact <- as.factor(grupos) #OJO: para este test se requiere que la variable de clasificaci�n sea tipo factor
# kruskal.test(casos ~ gruposFact)
# # Evaluar el valor p y comparar con alfa
# -----------------------------------------------------------------------
