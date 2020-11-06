import pandas as pd

class DataProcess(object):
    """Class with all the methods required in a typical data science pipeline
    """
    
    def __init__(self, path, format='csv'):
        """ Constructor of the data process class.

        Args:
            path (pathlib/str): Full path where the input dataset is located.
            format (str, optional): File format of the input dataset. Defaults to 'csv'.
        """
        if format == 'csv':
            dataset = pd.read_csv(path)
        else:
            raise ValueError("Input file format not supported")

        self.dataset = dataset
        self.is_standardize = False

        self.continuos_cols = 0 # Numerical (quantitative)
        self.discrete = 0       # Numerical (quantitative)
        self.categorical = 0    # Numerical or char (qualitative)

    def __str__(self):
        print("Position | Column name:")
        for index, col in enumerate(self.dataset.columns):
            print(f"{index} | {col}")
        print()
        total_rows = len(self.dataset.index)
        total_col = len(self.dataset.columns)

        return f"Data frame with {total_col} columns and {total_rows} rows in total"

    def save(self, path, format='csv'):
        if format == 'csv':
            self.dataset.to_csv(path)
        elif format == 'json':
            self.dataset.to_json(path)
        elif format == 'xlsx':
            self.dataset.to_excel(path)
        else:
            raise ValueError("Output file format not supported")

    def describe(self, graph=False, compact=False):
        if compact:
            self.dataset.describe(include="all")
        else:
            for col in self.dataset.columns:
                print("="*27)
                print(col)
                print("="*27)
                print(self.dataset[col].describe())
                print("")
    
    def remove_cols(self, cols_to_remove):
        if cols_to_remove is all numeric: # TODO: Finish this.
            self.dataset.drop(self.dataset.columns[cols_to_remove], axis=1)
        else:
            self.dataset.drop(cols_to_remove, axis=1)

    def rename_cols(self, cols_to_rename):
        pass

    def unify_format(self, cols, search_func, transform_func):
        pass

    def standardize(self, cols, method):

        self.is_standardize = True
        pass

    def reduction_dims(self, cols, method='PCA'):
        if not is_standardize:
            raise ValueError("You should standardize your columns first.")
        pass

    def clusterization(self, method='k-means'):
        pass

    