import os
from pathlib import Path

from data_process import DataProcess


project_path = Path(os.getcwd())
sysarmy_survey = project_path / "data/raw/2020.2 - sysarmy - Encuesta de remuneración salarial Argentina.csv"

sysarmy_analysis = DataProcess(sysarmy_survey, 'csv')
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
]
sysarmy_analysis.remove_cols(cols_to_remove)
print(sysarmy_analysis)


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
print(sysarmy_analysis)