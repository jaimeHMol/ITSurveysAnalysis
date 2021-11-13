import os
from pathlib import Path

from data_process import DataProcess

project_path = Path(os.getcwd())
output_path = project_path / "data/prepared/"


# ----------------------------------------------------------------------------------
# Data load
stackoverflow_survey = project_path / "data/raw/survey_results_public.csv"
stackoverflow_analysis = DataProcess(stackoverflow_survey, 'csv')


# ----------------------------------------------------------------------------------
# Data refine and exploration
print(stackoverflow_analysis)

cols_to_remove = [
    'Respondent',
    'SurveyEase',
    'SurveyLength',
    'SOVisitFreq',
    'SOPartFreq',
    'SOComm',
    'SOAccount',
    'PurchaseWhat',
    'NEWSOSites',
    'NEWStuck',
    'NEWPurpleLink',
    'NEWPurchaseResearch',
    'NEWOvertime',
    'NEWOtherComms',
    'NEWOnboardGood',
    'NEWOffTopic',
    # 'NEWLearn',
    'NEWJobHuntResearch',
    'NEWJobHunt',
    'JobFactors',
    'SOPartFreq',
    'SOPartFreq',
    'SOPartFreq',
    'SOPartFreq',
]
stackoverflow_analysis.remove_cols(cols_to_remove)
print(stackoverflow_analysis)
# stackoverflow_analysis.describe(graph=True)

numeric_types = ['int32', 'int64', 'float32', 'float64']
cols_by_type = stackoverflow_analysis.group_cols_by_type()
cols_numeric = stackoverflow_analysis.get_cols_by_type(cols_by_type, numeric_types)
all_cols = list(stackoverflow_analysis.dataset.columns)

# cols_to_unify = [
#     'Plataformas',
# ]
# str_to_replace = {
#     'ninguna de las anteriores': '', 
# }
# stackoverflow_analysis.unify_cols(cols_to_unify, 'technologies', str_to_replace)

# stackoverflow_analysis.remove_cols(cols_to_unify)

# stackoverflow_analysis.explore(compact=True)

stackoverflow_analysis.replace_missing(all_cols, method='remove')
stackoverflow_analysis.replace_outliers(cols_numeric, method='drop_iqr')
# stackoverflow_analysis.describe(graph=True)

            
# ----------------------------------------------------------------------------------
# Data processing
all_cols_to_standard = cols_numeric

stackoverflow_analysis.standardize(all_cols_to_standard, 'z_score')

# Dimensionality reduction using PCA:
# Applies only for numeric columns, requires standardized values
stackoverflow_analysis.reduction_dims(
    all_cols_to_standard,
    method='pca', 
    final_number_dims=2, 
    visualize=True
)

stackoverflow_analysis.clusterization(
    all_cols_to_standard,
    method='dbscan', 
    visualize=True
)

# stackoverflow_analysis.dummy_cols_from_text(col='technologies', sep=',', n_cols=15)
# print(stackoverflow_analysis)


# ----------------------------------------------------------------------------------
# stackoverflow_analysis.reset()
# print(stackoverflow_analysis)

# stackoverflow_analysis.save(output_path / 'stackoverflow_survey_analysed.csv')
# print(stackoverflow_analysis)