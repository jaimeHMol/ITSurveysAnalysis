import logging
import math
import webbrowser
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from kneed import KneeLocator
from pandas.api.types import is_numeric_dtype
from pandas_profiling import ProfileReport
from prince import MCA
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn_extra.cluster import KMedoids

# TOIMPROVE: Add optional argument "cols" to all the method that do some process over the self.dataset
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class DataProcess(object):
    """Class with all the methods required in a typical data science pipeline
    """
    # pandas.options.mode.use_inf_as_na = True
    numeric_types = ["uint8", "uint16", "uint32", "uint64", "int8", "int16", "int32", "int64", "float8", "float16", "float32", "float64"]
    categoric_types = ["object", "category"]

    def __init__(self, path, format="csv", log_level=logging.WARNING):
        """ Constructor of the data process class.

        Args:
            path (pathlib/str): Full path (including file name) where the input dataset is located.
            format (str, optional): File format of the input dataset. Defaults to "csv".
        """

        if format == "csv":
            dataset = pd.read_csv(path)
        else:
            raise ValueError("Input file format not supported")
        self.path = path
        self.input_file_name = path.stem
        self.input_file_format = format
        self.dataset = dataset
        self.dataset_raw = dataset.copy(deep=True)
        
        # TOIMPROVE: Fill this in a more comprehensive way.
        self.is_standardize = False
        self.continuos_cols = 0 # Numerical (quantitative)
        self.discrete = 0       # Numerical (quantitative)
        self.categorical = 0    # Numerical or char (qualitative)
        
        # TODO: Not working for all the methods of the class. Temporally setting log level at module level
        # logger.setLevel(log_level)


    def __str__(self):
        # logger.info("Position | Column name:")
        # for index, col in enumerate(self.dataset.columns):
        #     logger.info(f"{index} | {col}")
        # logger.info()
        # total_rows = len(self.dataset.index)
        # total_col = len(self.dataset.columns)
        # return f"Data frame with {total_col} columns and {total_rows} rows in total"

        self.dataset.info()

        return ""


    def save(self, path, format="csv"):
        if format == "csv":
            self.dataset.to_csv(path)
        elif format == "json":
            self.dataset.to_json(path)
        elif format == "xlsx":
            self.dataset.to_excel(path)
        else:
            raise ValueError("Output file format not supported")


    def describe(self, graph=False, compact=False):
        if compact:
            self.dataset.describe(include="all")
        else:
            for col in self.dataset.columns:
                logger.info("="*27)
                logger.info(col)
                logger.info("="*27)
                logger.info(self.dataset[col].describe())
                logger.info("")
        if graph:
            cols_by_type = self.group_cols_by_type()
            cols_numeric = self.get_cols_by_type(cols_by_type, self.numeric_types)
            cols_categoric = self.get_cols_by_type(cols_by_type, self.categoric_types)

            self.graph_numeric_cols(cols_numeric)
            self.graph_categoric_cols(cols_categoric)


    def graph_numeric_cols(self, cols_numeric):
        cols_numeric_count = len(cols_numeric)
        fig, axs = plt.subplots(cols_numeric_count, 1, figsize=(7, cols_numeric_count))
        for index, col in enumerate(cols_numeric):
            values = self.dataset[col]
            if values.isnull().values.any():
                logger.info(f"WARNING: The column {col} has NaN values that were dropped just to build the box plot.")
                values = values.dropna()
            axs[index].set_title(f"{col} - type: {values.dtype}")
            axs[index].boxplot(values, vert=False)
            axs[index].get_xaxis().set_visible(False)
            axs[index].get_yaxis().set_visible(False)
        fig.tight_layout()
        plt.show()           


    def graph_categoric_cols(self, cols_categoric):
        cols_categoric_count = len(cols_categoric)

        ncols = 2
        nrows = math.ceil(cols_categoric_count / ncols)
        fig, axs = plt.subplots(nrows, ncols, squeeze=False, figsize=(7, 3*nrows))

        x_index = 0
        y_index = 0
        for index, col in enumerate(cols_categoric):
            if index % ncols == 0 and index > 0:
                x_index = 0
                y_index += 1

            axs[y_index, x_index].set_title(col)

            data = self.dataset[col].value_counts(dropna=False)
            mapper_to_rename = {str(x): str(x) if len(str(x))<10 else str(x)[0:9]+".." for x in data.index}
            data_cat_renamed = data.rename(mapper_to_rename)

            data_cat_renamed.plot(kind="bar", ax=axs[y_index, x_index])

            if len(data_cat_renamed) > 6:
                axs[y_index, x_index].get_xaxis().set_ticklabels([])
                axs[y_index, x_index].get_yaxis().set_visible(False)
            x_index += 1
        
        if cols_categoric_count % ncols != 0:
            axs[-1, -1].axis("off")
        fig.tight_layout()
        plt.show()           


    def explore(self, output_path=None, name_postfix="report", compact=False):
    #     #!pip install sweetviz
    #     import sweetviz as sv
    #     dataset_report = sv.analyze(self.dataset)
    #     dataset_report.show_html(filepath=f"{output_path}dataset_report.html", open_browser=True)
     
        if output_path is None:
            output_path =  f"{self.input_file_name}_{name_postfix}.html"
        dataset_report = ProfileReport(self.dataset, title=f"{self.input_file_name} Report", minimal=compact)
        dataset_report.to_file(f"{output_path}")
        webbrowser.open(f"{output_path}")



    def drop_cols(self, cols):
        if all(isinstance(item, int) for item in cols):
            col_names = self.dataset.columns[cols]
            self.dataset = self.dataset.drop(col_names, axis=1)
        else:
            self.dataset = self.dataset.drop(cols, axis=1)


    def rename_cols(self, cols):
        self.dataset = self.dataset.rename(mapper=cols, axis=1)


    def reformat_cols(self, cols):
        pass


    def unify_format(self, cols, search_func, transform_func):
        pass

    
    def enforce_numeric(self, cols):
        for col in cols:
            self.dataset[col] = pd.to_numeric(self.dataset[col], errors="coerce")


    def categories_to_num(self, cols):
        for col in cols:
            self.dataset[f"{col}_num"] = pd.Categorical(self.dataset[col]).codes


    def replace_str_in_col(self, col, str_to_replace):
        for str_find, str_rep in str_to_replace.items():
            self.dataset[col] = self.dataset[col].apply(lambda x: str(x).replace(str_find, str_rep) if pd.notnull(x) else x)


    def unify_cols(self, cols, new_col, str_to_replace={";":"", ".":""}):
        for col in cols:
            self.dataset[col] = self.dataset[col].replace(np.nan, "").str.strip().str.lower()       
            self.replace_str_in_col(col, str_to_replace)
        self.dataset[new_col] = self.dataset[cols].agg(",".join, axis=1)


    def group_cols_by_type(self):        
        dataset_series = self.dataset.columns.to_series()
        cols_by_type = dataset_series.groupby(self.dataset.dtypes).groups
        cols_by_type = {str(key): list(value) for key, value in cols_by_type.items()}
        return cols_by_type


    def get_cols_by_type(self, cols_by_type, types):
        grouped_cols = []
        for type in types: 
            if cols_by_type.get(type): 
                grouped_cols.extend(cols_by_type.get(type))
        return grouped_cols


    def handle_missing(self, cols, method="mode", constant=None):
        """ Look for all NaN values (nulls, none, blanks) in the input columns and replace
        them according to the method selected. If you define method = "drop" all the 
        rows with one or more NaN will be deleted from the dataset.
        """
        # HINT: Be careful with datetime columns, since they use NaT instead of NaN
        logger.info("")
        for col in cols:
            na_count = self.dataset[col].isna().sum()
            if method == "mode":
                current_mode = self.dataset[col].mode(dropna=True)
                self.dataset[col] = self.dataset[col].fillna(current_mode)
                logger.warning(f"{na_count} values replaced in column {col} because missing values.")
            elif method == "mean":
                current_mean = self.dataset[col].mean()
                self.dataset[col] = self.dataset[col].fillna(current_mean)
                logger.warning(f"{na_count} values replaced in column {col} because missing values.")
            elif method == "median":
                current_median = self.dataset[col].median()
                self.dataset[col] = self.dataset[col].fillna(current_median)
                logger.warning(f"{na_count} values replaced in column {col} because missing values.")
            elif method == "drop":
                self.dataset = self.dataset.dropna(subset=[col])
                logger.warning(f"{na_count} rows dropped because missing values in column {col}.")
            elif method == "constant" and constant:
                self.dataset[col] = self.dataset[col].fillna(constant)
                logger.warning(f"{na_count} values replaced in column {col} because missing values.")
            else:
                raise ValueError("Replace missing values method not implemented or required input not provided.")


    def handle_outliers(self, cols, method="drop_iqr"):
        """ Look for outliers and handle them according to the method received.
            Only works for numeric columns
        """
        logger.info("")
        numeric_cols = (col for col in cols if is_numeric_dtype(self.dataset[col]))
        for col in numeric_cols:        
            row_count_ini = len(self.dataset[col])
            skew = self.dataset[col].skew()
            logger.info(f"Column {col} original skew value: {skew}")
            if -1 < skew < 1:
                logger.info(f"Column {col} doesn't seem to have outliers (regular skew value between -1 and 1. Assuming data have normal distribution.")                
                continue

            if method == "replace_10_90_min_max":
                min = self.dataset[col].quantile(0.10)
                max = self.dataset[col].quantile(0.90)
                self.dataset[col] = np.where(self.dataset[col] < min, min, self.dataset[col])
                self.dataset[col] = np.where(self.dataset[col] > max, max, self.dataset[col])
                # TODO: Print count of rows replaced.
            elif method == "replace_5_95_median":
                median = self.dataset[col].quantile(0.5)
                min = self.dataset[col].quantile(0.05)
                max = self.dataset[col].quantile(0.95)
                self.dataset[col] = np.where(self.dataset[col] < min, median, self.dataset[col])
                self.dataset[col] = np.where(self.dataset[col] > max, median, self.dataset[col])
                # TODO: Print count of rows replaced.
            elif method == "drop_10_90":
                min = self.dataset[col].quantile(0.10)
                max = self.dataset[col].quantile(0.90)
                self.dataset = self.dataset.query(f"{col} >= {min} and {col} <= {max}")
                row_count_fin = len(self.dataset[col])
                row_count_dif = row_count_ini - row_count_fin
                logger.warning(f"{row_count_dif} rows dropped because outliers in column {col}.")
            elif method == "drop_5_95":
                min = self.dataset[col].quantile(0.05)
                max = self.dataset[col].quantile(0.95)
                self.dataset = self.dataset.query(f"{col} >= {min} and {col} <= {max}")
                row_count_fin = len(self.dataset[col])
                row_count_dif = row_count_ini - row_count_fin
                logger.warning(f"{row_count_dif} rows dropped because outliers in column {col}.")
            elif method == "drop_iqr":
                q1 = self.dataset[col].quantile(0.25)
                q3 = self.dataset[col].quantile(0.75)
                iqr = q3 - q1
                min = q1 - 1.5 * iqr
                max = q3 + 1.5 * iqr
                self.dataset = self.dataset.query(f"{col} >= {min} and {col} <= {max}")
                row_count_fin = len(self.dataset[col])
                row_count_dif = row_count_ini - row_count_fin
                logger.warning(f"{row_count_dif} rows dropped because outliers in column {col}.")
            else:
                raise ValueError("Outliers handling method not implemented.")
            skew = self.dataset[col].skew()
            logger.info(f"Column {col} final skew value: {skew}. Between -1 and 1 the best. Assumes data have normal distribution.")


    def handle_zeros(self, cols, method="drop", constant=None):
        """ Look for zeros and handle them according to the method received.
            Only works for numeric columns
        """
        logger.info("")
        numeric_cols = (col for col in cols if is_numeric_dtype(self.dataset[col]))
        for col in numeric_cols:      
            row_count_ini = len(self.dataset[col])
            if method == "mode":
                current_mode = self.dataset[col].mode(dropna=True)
                self.dataset[col] = self.dataset[col].replace({0: current_mode})
                # TODO: Print count of rows replaced.
            elif method == "mean":
                current_mean = self.dataset[col].mean()
                self.dataset[col] = self.dataset[col].replace({0: current_mean})
                # TODO: Print count of rows replaced.
            elif method == "median":
                current_median = self.dataset[col].median()
                self.dataset[col] = self.dataset[col].replace({0: current_median})
                # TODO: Print count of rows replaced.
            elif method == "constant" and constant:
                self.dataset[col] = self.dataset[col].replace({0: constant})
                # TODO: Print count of rows replaced.
            elif method == "drop":
                self.dataset = self.dataset.query(f"{col} != 0")
                row_count_fin = len(self.dataset[col])
                row_count_dif = row_count_ini - row_count_fin
                logger.warning(f"{row_count_dif} rows dropped because zeros in column {col}.")
            else:
                raise ValueError("Zeros handling method not implemented or required input not provided.")


    def standardize(self, cols, method="z_score"):
        if method == "z_score":
            for col in cols:
                # TODO: Confirm that this transformation is working correctly
                # it doesn't look like is working with column "experiencia_anios"
                self.dataset[col] = (self.dataset[col] - self.dataset[col].mean() / self.dataset[col].std())
            self.is_standardize = True            
        elif method == "0-1":
            # self.is_standardize = True
            pass
        else:
            raise ValueError("Standardize method not supported")
            

    # TODO: Implement using SOLID.
    def reduction_dims(self, cols=None, method="pca", final_number_dims=2, visualize=True):
        if not self.is_standardize:
            raise ValueError("You should standardize your columns first.")
        if not cols:
            # Will use all the columns of the dataset on the dim reduction analysis
            cols = self.dataset.columns.tolist()

        if method == "pca":
            pca = PCA(n_components=final_number_dims)
            principal_components = pca.fit_transform(self.dataset[cols])

            for index in range(0, final_number_dims):
                self.dataset[f"PC{index + 1}"] = principal_components[:,index]

            logger.info("Principal components analysis finished. Explained variance ratio:")
            components_variance = ["{:.12f}".format(i)[:8] for i in pca.explained_variance_ratio_]
            logger.info(components_variance)

            if visualize and final_number_dims == 2:
                x = self.dataset["PC1"]
                y = self.dataset["PC2"]
                scalex = 1.0/(x.max() - x.min())
                scaley = 1.0/(y.max() - y.min())
                coeff = np.transpose(pca.components_)

                fig = plt.figure(figsize = (8,8))
                sp = fig.add_subplot(1,1,1) 
                sp.set_xlabel(f"PC 1 - Variance ratio: {components_variance[0]}", fontsize = 15)
                sp.set_ylabel(f"PC 2 - Variance ratio: {components_variance[1]}", fontsize = 15)
                sp.set_xlim(-1,1)
                sp.set_ylim(-1,1)
                sp.set_title("PCA Biplot", fontsize = 20)
                sp.scatter(x * scalex, y * scaley, s = 50)
                for i, col in enumerate(cols):
                    plt.arrow(0, 0, coeff[i,0], coeff[i,1], color = "r", head_width=0.02, length_includes_head = True)
                    plt.text(coeff[i,0] /2, coeff[i,1] /2, col, color = "g", ha = "left", va = "baseline")
                sp.grid()
                plt.show()

        elif method == "mca":
            mca = MCA(n_components=final_number_dims)
            dataset_mca = mca.fit_transform(self.dataset[cols])

            for index in range(0, final_number_dims):
                self.dataset[f"MC{index + 1}"] = dataset_mca[index]

            logger.info("Multiple correspondence analysis finished. Explained variance ratio:")
            mca_variance = ["{:.12f}".format(i)[:8] for i in mca.explained_inertia_]
            logger.info(mca_variance)

            if visualize and final_number_dims == 2:
                mca.plot_coordinates(X=self.dataset[cols])
        else:
            raise ValueError("Method of dimensionality reduction not implemented.")


    # TODO: Implement this using SOLID
    def clusterization(self, cols=None, method="k_means", visualize=True, n_clusters=None):

        if not self.is_standardize:
            raise ValueError("You should standardize your columns first.")

        if method == "k_means":
            logger.info("="*27)
            logger.info("Clustering using K-Means")
            logger.info("="*27)

            kmeans_kwargs  = {
                "init": "random",
                "n_init": 10,
                "max_iter": 300,
                "random_state": 42,
            }
            sse = []
            kmeans_silhouette_coefficients = []
            for k in range(2, 11):
                kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
                kmeans.fit(self.dataset[cols])
                sse.append(kmeans.inertia_)
                score = silhouette_score(self.dataset[cols], kmeans.labels_)
                kmeans_silhouette_coefficients.append(score)

            if visualize:
                # plt.style.use("fivethirtyeight")
                plt.plot(range(2, 11), sse)
                plt.xticks(range(2, 11))
                plt.title("K-Means")
                plt.xlabel("Number of Clusters")
                plt.ylabel("SSE")
                plt.show()

                # plt.style.use("fivethirtyeight")
                plt.plot(range(2, 11), kmeans_silhouette_coefficients)
                plt.xticks(range(2, 11))
                plt.title("K-Means")
                plt.xlabel("Number of Clusters")
                plt.ylabel("Silhouette Coefficient")
                plt.show()

            kl = KneeLocator(range(2, 11), sse, curve="convex", direction="decreasing")
                
            number_clusters_best = kl.elbow
            logger.info(f"Best number of clusters using elbow method: {number_clusters_best}")
            logger.info("")
            logger.info(f"See the graph Silhouette coefficient vs number of clusters to define \
                the best amount of clusters in your case. \
                (Silhouette coefficient goes from -1 to 1, near to 1 is better)")
            logger.info("")

        elif method == "k_medoids":
            logger.info("="*27)
            logger.info("Clustering using K-Medoids")
            logger.info("="*27)

            kmedoids_kwargs  = {
                "metric": "euclidean",
            }
            sse = []
            kmedoids_silhouette_coefficients = []
            for k in range(2, 11):
                kmedoids = KMedoids(n_clusters=k, **kmedoids_kwargs)
                kmedoids.fit(self.dataset[cols])
                sse.append(kmedoids.inertia_)
                score = silhouette_score(self.dataset[cols], kmedoids.labels_)
                kmedoids_silhouette_coefficients.append(score)

            if visualize:
                # plt.style.use("fivethirtyeight")
                plt.plot(range(2, 11), sse)
                plt.xticks(range(2, 11))
                plt.title("K-Medoids")
                plt.xlabel("Number of Clusters")
                plt.ylabel("SSE")
                plt.show()

                # plt.style.use("fivethirtyeight")
                plt.plot(range(2, 11), kmedoids_silhouette_coefficients)
                plt.xticks(range(2, 11))
                plt.title("K-Medoids")
                plt.xlabel("Number of Clusters")
                plt.ylabel("Silhouette Coefficient")
                plt.show()

            kl = KneeLocator(range(2, 11), sse, curve="convex", direction="decreasing")
                
            number_clusters_best = kl.elbow
            logger.info(f"Best number of clusters using elbow method: {number_clusters_best}")
            logger.info("")
            logger.info(f"See the graph Silhouette coefficient vs number of clusters to define \
                the best amount of clusters in your case. \
                (Silhouette coefficient goes from -1 to 1, near to 1 is better)")
            logger.info("")

        elif method == "dbscan":
            logger.info("="*27)
            logger.info("Clustering using DBScan")
            logger.info("="*27)

            silhouette_eps_ncluster = {}
            for eps in np.linspace(0.1, 4, 10):
                dbscan = DBSCAN(eps=eps)
                dbscan.fit(self.dataset[cols])
                if len(set(dbscan.labels_)) > 1:
                    # Silhouette score requires at least 2 clusters to be calculated.
                    # Rows marked with dbscan.labels_=-1 don"t belong to a real cluster
                    # but are considered noise.
                    score = round(silhouette_score(self.dataset[cols], dbscan.labels_), 4)
                    nclusters = len(set(dbscan.labels_))
                    
                    silhouette_eps_ncluster[score] = ((eps, nclusters))

            if visualize:
                y, tup = zip(*silhouette_eps_ncluster.items())
                x = [eps for eps, nclusters in tup]

                # plt.style.use("fivethirtyeight")
                plt.plot(x, y)
                plt.xticks(np.linspace(0.1,4,10))
                plt.title("DBScan")
                plt.xlabel("eps")
                plt.ylabel("Silhouette Coefficient")
                plt.show()

            nclusters_best = silhouette_eps_ncluster.get(max(silhouette_eps_ncluster.keys()), -1)[1]
            logger.info(f"Best number of clusters using Silhouette over multiple eps: {nclusters_best}")
            logger.info("")

            # TODO: Add column with the id of the cluster each row belongs to
            # TODO: Implement scatter plot of clusters.
        else:
            raise ValueError("Clustering method not implemented.")
        

    def dummy_cols_from_text(self, col, sep=",", n_cols=10):
        if self.dataset[col].dtype == np.number:
            raise ValueError("The origin column to generate dummy columns must be text.")

        dummy_df = self.dataset[col].str.get_dummies(sep=sep)

        top_dummy_df = dummy_df[dummy_df.sum().sort_values(ascending=False, inplace=False)[0:n_cols].index]

        self.dataset = pd.concat([self.dataset, top_dummy_df], axis=1, sort=False)


    def dummy_cols_from_category(self, cols, drop_first=False):
        for col in cols:
            dummy_df = pd.get_dummies(self.dataset[col], prefix=f"{col}", drop_first=drop_first)
            self.dataset = pd.concat([self.dataset, dummy_df], axis=1, sort=False)    


    def linear_regression(self, col_to_predict, cols=[], cols_to_remove=[], graph=True, num_vars_graph=10):
        if cols:
            cols_numeric = cols
        else:
            cols_by_type = self.group_cols_by_type()
            # Linear regression only works with numeric columns
            cols_numeric = self.get_cols_by_type(cols_by_type, self.numeric_types)
            # xs = self.dataset.drop([col_to_predict], axis=1)
        if col_to_predict in cols_numeric: cols_numeric.remove(col_to_predict)
        for col in cols_to_remove:
            if col in cols_numeric: cols_numeric.remove(col)

        logger.info("*** Training linear regression model...")
        X_train, X_test, y_train, y_test = train_test_split(
            self.dataset[cols_numeric],
            self.dataset[col_to_predict],
            random_state = 777
        )

        reg = LinearRegression()
        reg.fit(X_train, y_train)
        prediction = reg.predict(X = X_test)

        logger.info("")
        logger.info("R2 coefficient (Using training data): ")
        logger.info(r2_score(y_true=y_test, y_pred=prediction))

        mse = mean_squared_error(
            y_true  = y_test,
            y_pred  = prediction,
            squared = False
        )
        logger.info("The error (MSE) in test is: ")
        logger.info("mse")
        logger.info("")

        # Get importance. In this model the absolute value measures the importance of 
        # each feature.
        importances = tuple(abs(item) for item in reg.coef_)
        # Summarize feature importance.
        cols_importance = list(zip(cols_numeric, importances))
        cols_importance_ordered = sorted(cols_importance, key=lambda x: x[1], reverse=True)

        for col, importance in cols_importance_ordered:
            logger.info(f"Feature: {col}, Score: {importance}")

        if graph:
            x_axis = ["\n".join(wrap(x, 20)) for x in list(zip(*cols_importance_ordered))[0][:num_vars_graph]]
            y_axis = list(zip(*cols_importance_ordered))[1][:num_vars_graph]
            plt.figure(figsize=(9,4))
            plt.title("Feature Importance - Linear Regression")
            plt.bar(x_axis, y_axis)
            plt.xticks(rotation=90)
            plt.margins(x=0, y=0.1)
            plt.show()
            reg.top_vars_graph = zip(x_axis, y_axis)
        
        return reg


    def random_forest(self, col_to_predict, cols=[], cols_to_remove=[], graph=True, num_vars_graph=10):
        if cols:
            cols_input = cols
        else:
            # TODO: Validate if random forest requires all variables to be numeric (no categoric).
            cols_input = list(self.dataset)
        if col_to_predict in cols_input: cols_input.remove(col_to_predict)
        for col in cols_to_remove:
            if col in cols_input: cols_input.remove(col)

        logger.info("*** Training random forest model...")
        X_train, X_test, y_train, y_test = train_test_split(
            self.dataset[cols_input],
            self.dataset[col_to_predict],
            random_state = 777
        )
        model = RandomForestRegressor(
            n_estimators = 10,
            criterion    = 'mse',
            max_depth    = None,
            max_features = 'auto',
            oob_score    = False,
            n_jobs       = -1,
            random_state = 777
        )

        model.fit(X_train, y_train)
        prediction = model.predict(X = X_test)

        logger.info("")
        logger.info("R2 coefficient (Using test data): ")
        logger.info(r2_score(y_true=y_test, y_pred=prediction))

        mse = mean_squared_error(
            y_true  = y_test,
            y_pred  = prediction,
            squared = False
        )
        logger.info("The error (MSE) in test is: ")
        logger.info(mse)
        logger.info(f"")


        # Get importance
        importances = model.feature_importances_
        # Summarize feature importance.
        cols_importance = list(zip(cols_input, importances))
        cols_importance_ordered = sorted(cols_importance, key=lambda x: x[1], reverse=True)

        for col, importance in cols_importance_ordered:
            logger.info(f"Feature: {col}, Score: {importance}")
        
        if graph:
            x_axis = ["\n".join(wrap(x, 20)) for x in list(zip(*cols_importance_ordered))[0][:num_vars_graph]]
            y_axis = list(zip(*cols_importance_ordered))[1][:num_vars_graph]
            plt.figure(figsize=(9,4))
            plt.title("Feature Importance - Random Forest")
            plt.bar(x_axis, y_axis)
            plt.xticks(rotation=90)
            plt.margins(x=0, y=0.1)
            plt.show()
            model.top_vars_graph = zip(x_axis, y_axis)

        return model


    def reset (self):
        self.__init__(self.path, self.input_file_format)
