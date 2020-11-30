import os
from pathlib import Path

from data_process import DataProcess


# Data load
project_path = Path(os.getcwd())
sysarmy_survey = project_path / "data/raw/2020.2 - sysarmy - Encuesta de remuneración salarial Argentina.csv"
output_path = project_path / "data/prepared/"

sysarmy_analysis = DataProcess(sysarmy_survey, 'csv')


# Data refine and exploration
print(sysarmy_analysis)

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
    'QA / Testing',
]
sysarmy_analysis.remove_cols(cols_to_remove)
print(sysarmy_analysis)

cols_to_rename = {
    'Me identifico': 'genero',
    'Tengo': 'edad',
    'Dónde estás trabajando': 'ubicacion',
    'Años de experiencia': 'experiencia_anios',
    'Años en la empresa actual': 'empresa_actual_anios',
    'Nivel de estudios alcanzado': 'max_nivel_estudios',
    '¿Gente a cargo?': 'personas_a_cargo',
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
print(sysarmy_analysis)
# sysarmy_analysis.describe(graph=True)

numeric_types = ['int32', 'int64', 'float32', 'float64']
cols_by_type = sysarmy_analysis.group_cols_by_type()
cols_numeric = sysarmy_analysis.get_cols_by_type(cols_by_type, numeric_types)

cols_to_unify = [
    'Plataformas',
    'Lenguajes de programación', 
    'Frameworks, herramientas y librerías',
    'Bases de datos',
    'IDEs'
]
chr_to_replace = {';':'', '.':'', 'ninguno':'', 'ninguna':''}
sysarmy_analysis.unify_cols(cols_to_unify, 'tecnologies', chr_to_replace)

sysarmy_analysis.remove_cols(cols_to_unify)

sysarmy_analysis.explore()


# Data processing
all_cols_to_standard = cols_numeric

cols_to_standard = [
    'edad', 
    'experiencia_anios' ,
    'empresa_actual_anios', 
    'personas_a_cargo',
    'sueldo_conformidad',
    'sueldo_mensual_bruto_ars',
    'sueldo_ajuste_total_2020',
    'recomendacion_laboral',
    'politicas_diversidad'
]
sysarmy_analysis.standardize(cols_to_standard, 'z_score')

# Dimensionality reduction using PCA:
# Applies only for numeric columns, requieres standardized values
sysarmy_analysis.reduction_dims(
    cols_to_standard,
    method='pca', 
    final_number_dims=2, 
    visualize=True
)

sysarmy_analysis.clusterization(
    cols_to_standard,
    method='k_means', 
    visualize=True
)



# sysarmy_analysis.reset()
# print(sysarmy_analysis)

# sysarmy_analysis.save(output_path / 'sysarmy_survey_analysed.csv')
# print(sysarmy_analysis)


