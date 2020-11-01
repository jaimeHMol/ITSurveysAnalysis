

class DataProcess(object):
    """
    docstring
    """
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.is_standardize = False

        # TODO: Validate dataset is a panda object
        self.continuos_cols = 0 # Numerical (quantitative)
        self.discrete = 0       # Numerical (quantitative)
        self.categorical = 0    # Numerical or char (qualitative)

    def __str__(self):
        print("Position | Column name:")
        for index, col in enumerate(self.dataset):
            print(f"{index} | {col}")
        print()
        total_rows = 0
        print(f"Total rows {total_rows}")

    def describe(self, graph=False, verbose=False):
        pass
    
    def remove_cols(self, cols_to_remove):
        pass

    def rename_cols(self, cols_to_rename):
        pass

    def unify_format(self, cols, search_func, transform_func):
        pass

    def standardize(self, cols, method):

        self.is_standardize = True
        pass

    def reduction_dims(self, method='PCA', cols):
        if not is_standardize:
            raise ValueError("You should standardize your columns first.")
        pass

    def clusterization(self, method='k-means'):
        pass

    