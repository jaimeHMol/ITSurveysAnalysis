import os
from pathlib import Path
import numpy as np

from data_process import DataProcess

project_path = Path(os.getcwd())
output_path = project_path / "data/prepared/"

# ----------------------------------------------------------------------------------
# Data load
real_state_data = project_path / "data/raw/train.csv"
real_state_analysis = DataProcess(real_state_data, "csv")

print(real_state_analysis)


numeric_types = ["int32", "int64", "float32", "float64"]
cols_by_type = real_state_analysis.group_cols_by_type()
cols_numeric = real_state_analysis.get_cols_by_type(cols_by_type, numeric_types)


real_state_analysis.handle_missing(cols_numeric, method="median")


real_state_analysis.standardize(cols_numeric, "z_score")

cols_numeric.append("SalePrice")
cols_numeric.remove("LotArea")

# real_state_analysis.is_standardize = True
real_state_analysis.reduction_dims(
    cols_numeric,
    method="pca", 
    final_number_dims=2, 
    visualize=True
)
