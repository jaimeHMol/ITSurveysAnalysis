# -------------------------------------------------------------------------------------------------------------------
# Template Script Data Mining
# -------------------------------------------------------------------------------------------------------------------
# Plantilla con la estructura principal para un script en R para an�lisis de data mining / data science
# Creado en Julio de 2017
# @kingSelta
# -------------------------------------------------------------------------------------------------------------------

# ===================================================================================================================
# Inicio
# ===================================================================================================================

# ----------------
# Limpieza inicial
# ----------------
# Limpia memoria
rm( list=ls() )
gc()

# Limpia consola
cat("\014") # Imprime de Form Feed character ("\f")

# -------------------------
# Almacena tiempo de inicio
# -------------------------
timeIni <- Sys.time()

# ----------------------------------------------------------------------------------
# Instalar paquetes (Solo se hace la primera vez que se va a utilizar una libreria)
# ----------------------------------------------------------------------------------
#install.packages('caret')
#install.packages('ggplot2')
#install.packages('readxl')
#install.packages('rJava')
#install.packages('xlsx')
#install.packages('ADGofTest')
#install.packages('nortest')
#install.packages('MASS')
#install.packages('pastecs')
#install.packages('boot')
#install.packages('dplyr')
#install.packages('Rcmdr')
#install.packages('reshape2')
#install.packages('car')
#install.packages('moments')

# ------------------
# Invocar librerias
# ------------------
library(stringr)

library(caret)
library(ggplot2)
library(xlsx)
library(readxl)
library(ADGofTest)
library(nortest)
library(MASS)
library(boot)
library(pastecs)
library(reshape2)
library(car)
library(Rcmdr)
library(moments)
#Se puede hacer tambi�n con require(libreria)

# -------------------------
# Invocar funciones propias
# -------------------------
source('R:\\Common\\descDataSet.R')
source('R:\\Common\\descGrafVars.R')
source('R:\\Common\\enviarNotificacion.R')


# -------------------
# Constantes globales
# -------------------
programa             <-  "SueldosITAr.R"
algoritmo            <-  ""
busqueda             <-  "" # B�squeda hiperpar�metros
estimacion           <-  "" # Estimaci�n de rendimiento del modelo clasificador
prob_training        <-  0.7
prob_testing         <-  1 - prob_training
semilla              <-  777677 # Para generaci�n de aleatoriedad

# TODO: Mejor la asignaci�n de los nombres y rutas a utilizar
archivo_entrada      <-  "E:\\0.Drive\\0.Acad�mico\\2.Maestr�a en Ciencia de Datos-UBA\\Trabajo integrador\\2020.1 - sysarmy - Encuesta de remuneraci�n salarial Argentina - Argentina.txt"
nombre_archivo       <-  str_split(programa,"\\.")
archivo_salida       <-  str_c("R:\\Work\\Salida", nombre_archivo[[1]][1])
archivo_auxiliar     <-  str_c("R:\\Work\\Auxiliar", nombre_archivo[[1]][1])
separador            <-  "|" #" "  ";"  "," 
decimal              <-  "."             
campo_id             <-  "" #(identificador �nico de cada fila)
campos_a_borrar      <-  c( ) #Variables (columnas) a borrar

# Info para mapear unidad virtual en windows (y trabajar as� con direcciones realtivas) ----
# Para mapear una unidad virtual (en este caso M:) a una ruta, ejecutar en CMD de Windows:
# (De manera temporal, solo existe hasta que se apaga el PC)
#   (ir a la carpeta a enlazar: CD "C:\Datamining") SUBST M: .
# (De manera permanente)
#   Se debe crear un .bat con la instrucci�n y copiarlo en la carpeta de inicio para 
#   que se ejecute siempre que arranque windows.
# ------------------------

# ------------------------
# Configuraciones globales
# ------------------------
# -- WORKING DIRECTORY
#setwd("R:\\") # Mi directorio de trabajo
#setwd('M:\\') # o apuntando a una unidad virtual creada (ideal para manejar rutas relativas)

# -- HOME DIRECTORY
#Sys.setenv(R_USER="R:\\")

# -- NOTIFICACION DE ERRORES a trav�s de pushbullet
#options(error = NULL) # Valor por defecto
options(error = function() {
  if(!exists("timeIni")){
    timeTotal <- "Desconocido"  
  }else{
    timeFin <- Sys.time()
    timeTotal <- timeFin - timeIni
    timeTotal <- round(as.numeric(timeTotal)/60,1)
  }
  
  enviarNotificacion(titulo = "Ejecuci�n R", 
                     mensaje = paste("El programa",programa,"finaliz� con error el d�a",Sys.time(),
                                     "\nError:", geterrmessage(),
                                     "\nTiempo de ejecuci�n:", timeTotal,"minutos"), 
                     severidad = "KO")
})

# -------------------
# Cargar datos fuente
# -------------------

# DESDE LA WEB. Requiere acceso a internet
#dfSource <- read.csv("http://astrostatistics.psu.edu/datasets/COMBO17.csv", header=T, stringsAsFactors=F)

# CSV que tiene cada muestra como  una columna
dfSource <- data.frame(read.csv2(file=archivo_entrada, sep=separador,  dec=decimal,  stringsAsFactors=FALSE))

# ARCHIVO PLANO en general # HINT: Con algunos files me ha fallado
# dfSource <- read.table(archivo_entrada, sep=separador, dec=decimal, header=TRUE)

# EXCEL que tiene cada muestra como  una columna
#dfSource <- read_excel(path=archivo_entrada, sheet=1)  

# MANUALMENTE
#An1 = c(84.99,84.02,84.38)
#An2 = c(85.15,85.13,84.88)
#An3 = c(84.72,84.48,85.16)
#An4 = c(84.2,84.1,84.55)
#dfSource <- data.frame(An1,An2,An3,An4)

# Operaciones de borrado/limpieza ---------------------------------
# Borrar variables del data set de entrada que no me interesan
#dfSource <- dfSource[ , !(names(dfSource) %in%   campos_a_borrar)] 

# Borrar variable de trabajo espec�fica 
#rm(var_a_borrar)

# Borrar todas las variables tmp utilizadas
#rm(list = ls(pattern = "^tmp"))

# Pasar variables a factores si es necesario
# ------------------------------------------


# ===================================================================================================================
# Exploraci�n de variables (columnas)
# ===================================================================================================================

# ----------------------------------------------------------------
# Descripci�n cuantitativa del data set de entrada y sus variables
# ----------------------------------------------------------------
# Llama a la funci�n personalizada que realiza la descripci�n cuantitativa del dataset
dfDescDS <- descDataSet(dfSource)

# Escribe en un excel el data frame de descripci�n del data set de entrada
# TODO: Hacer validaci�n de que existe la ruta y si no existe crearla para que no d� error
write.xlsx(x = dfDescDS, file = "R:\\Work\\descDfSource.xlsx",
           sheetName = "Descripcion", row.names = FALSE)

# --------------------------------
# Descripci�n gr�fica de variables
# --------------------------------
# Selecciona las variables del dataset que desea explorar graficamente
dfSourceVars <- dfSource[,1:4]
# Llama a la funci�n personalizada que realiza la descripci�n gr�fica
descGrafVars(dfSourceVars,cantFil = 2, maximizar = TRUE)


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

# Ejemplo filtros o joins de data frames:
#dfSourceTestBoonsri = dfSourceTest[dfSourceTest$location %in% c("Boonsri"), ]
#data.readings = data.readings %>% left_join(data.units, by = "measure")





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
cat(  
  linea, 
  gan$tiempo,
  vmaxdepth, 
  vminbucket,
  format(Sys.time(), "%Y%m%d %H%M%S"), 
  archivo_entrada, 
  clase_nomcampo, 
  programa, 
  algoritmo, 
  busqueda, 
  estimacion, # Si una variable tiene varios elementos, con $ (ej:gan$ganancias) los coloca uno debajo del otro
  "\n", sep="\t", file=archivo_salida, fill=FALSE, append=TRUE 
)



# ----------------------------------------
# Construcci�n y entrenamiento del modelo
# ----------------------------------------
# Ejecuci�n


linea <- linea+1


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
if(!exists("timeIni")){
  timeTotal <- "Desconocido"  
}else{
  timeFin <- Sys.time()
  timeTotal <- timeFin - timeIni
  timeTotal <- round(as.numeric(timeTotal)/60,1)
}
print(paste0("Tiempo de ejecuci�n: ", timeTotal," minutos"))

# --------------------------------------
# Notificar la finalizaci�n (Pushbullet)
# --------------------------------------
notTitulo    <- "Ejecuci�n R"
notMensaje   <- paste("El programa", programa, "finaliz� correctamente el d�a", Sys.time(),
                      "\nTiempo de ejecuci�n:", as.character(timeTotal), "minutos")
notSeveridad <- "OK" 
enviarNotificacion(notTitulo, notMensaje, notSeveridad)


# --------------------------------
# Limpiar memoria y cerrar sesi�n
# --------------------------------
rm( list=ls() )
gc()
#quit( save="no" )





# ===================================================================================================================
# Funciones locales
# ===================================================================================================================
#





# ---------------------
# Para hacer broma (XD)
# ----------------------
# # Siempre que haya un error en la ejecuci�n generar� un sonido (que tiende a volverse molesto XD)
# install.packages("beepr")
# library(beepr)
# options(error = function() { beep(9) } )
# 
# # Simulamos un error
# enviarNotificacion(titulo= "asa", mensaje = "dfasdf", severidad ="asda")
# 
# # Volver a dejarlo normal
# options(error = NULL )

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
