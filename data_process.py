import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
from pandas_profiling import ProfileReport
import webbrowser

# TOIMPROVE: Add optional argument 'cols' to all the method that do some process over the self.dataset

class DataProcess(object):
    '''Class with all the methods required in a typical data science pipeline
    '''
    # pandas.options.mode.use_inf_as_na = True

    def __init__(self, path, format='csv'):
        ''' Constructor of the data process class.

        Args:
            path (pathlib/str): Full path where the input dataset is located.
            format (str, optional): File format of the input dataset. Defaults to 'csv'.
        '''
        if format == 'csv':
            dataset = pd.read_csv(path)
        else:
            raise ValueError('Input file format not supported')
        self.path = path
        self.format = format
        self.dataset_raw = dataset
        self.dataset = self.dataset_raw
        
        # TOIMPROVE: Fill this in a more comprehensive way.
        self.is_standardize = False
        self.continuos_cols = 0 # Numerical (quantitative)
        self.discrete = 0       # Numerical (quantitative)
        self.categorical = 0    # Numerical or char (qualitative)


    def __str__(self):
        # print('Position | Column name:')
        # for index, col in enumerate(self.dataset.columns):
        #     print(f'{index} | {col}')
        # print()
        # total_rows = len(self.dataset.index)
        # total_col = len(self.dataset.columns)
        # return f'Data frame with {total_col} columns and {total_rows} rows in total'

        self.dataset.info()

        return ''


    def save(self, path, format='csv'):
        if format == 'csv':
            self.dataset.to_csv(path)
        elif format == 'json':
            self.dataset.to_json(path)
        elif format == 'xlsx':
            self.dataset.to_excel(path)
        else:
            raise ValueError('Output file format not supported')


    def describe(self, graph=False, compact=False):
        if compact:
            self.dataset.describe(include='all')
        else:
            for col in self.dataset.columns:
                print('='*27)
                print(col)
                print('='*27)
                print(self.dataset[col].describe())
                print('')
        if graph:
            numeric_types = ['int32', 'int64', 'float32', 'float64']
            categoric_types = ['object']
            cols_by_type = self.group_cols_by_type()
            cols_numeric = self.get_cols_by_type(cols_by_type, numeric_types)
            cols_categoric = self.get_cols_by_type(cols_by_type, categoric_types)

            self.graph_numeric_cols(cols_numeric)
            self.graph_categoric_cols(cols_categoric)


    def graph_numeric_cols(self, cols_numeric):
        cols_numeric_count = len(cols_numeric)
        fig, axs = plt.subplots(cols_numeric_count, 1, figsize=(7, cols_numeric_count))
        for index, col in enumerate(cols_numeric):
            values = self.dataset[col]
            if values.isnull().values.any():
                print(f'WARNING: The column {col} has NaN values that were removed just to build the box plot.')
                values = values.dropna()
            axs[index].set_title(f'{col} - type: {values.dtype}')
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
            mapper_to_rename = {str(x): str(x) if len(str(x))<10 else str(x)[0:9]+'..' for x in data.index}
            data_cat_renamed = data.rename(mapper_to_rename)

            data_cat_renamed.plot(kind='bar', ax=axs[y_index, x_index])

            if len(data_cat_renamed) > 6:
                axs[y_index, x_index].get_xaxis().set_ticklabels([])
                axs[y_index, x_index].get_yaxis().set_visible(False)
            x_index += 1
        
        if cols_categoric_count % ncols != 0:
            axs[-1, -1].axis('off')
        fig.tight_layout()
        plt.show()           


    def explore(self, output_path='', compact=False):
    #     #!pip install sweetviz
    #     import sweetviz as sv
    #     dataset_report = sv.analyze(self.dataset)
    #     dataset_report.show_html(filepath=f'{output_path}dataset_report.html', open_browser=True)
     
        dataset_report = ProfileReport(self.dataset, title='Dataset Report', minimal=compact)
        dataset_report.to_file(f'{output_path}dataset_report.html')
        webbrowser.open(f'{output_path}dataset_report.html')



    def remove_cols(self, cols_to_remove):
        if all(isinstance(item, int) for item in cols_to_remove):
            col_names = self.dataset.columns[cols_to_remove]
            self.dataset = self.dataset.drop(col_names, axis=1)
        else:
            self.dataset = self.dataset.drop(cols_to_remove, axis=1)


    def rename_cols(self, cols_to_rename):
        self.dataset = self.dataset.rename(mapper=cols_to_rename, axis=1)


    def unify_format(self, cols, search_func, transform_func):
        pass


    def unify_cols(self, cols, new_col, str_to_replace={';':'', '.':''}):
        for col in cols:
            self.dataset[col] = self.dataset[col].replace(np.nan, '').str.strip().str.lower()
            
            for str_find, str_rep in str_to_replace.items():
                self.dataset[col] = self.dataset[col].apply(lambda x: x.replace(str_find, str_rep))

        self.dataset[new_col] = self.dataset[cols].agg(','.join, axis=1)


    def group_cols_by_type(self):        
        dataset_series = self.dataset.columns.to_series()
        cols_by_type = dataset_series.groupby(self.dataset.dtypes).groups
        cols_by_type = {str(key): list(value) for key, value in cols_by_type.items()}
        return cols_by_type


    def get_cols_by_type(self, cols_by_type, types):
        numeric_cols = []
        for key in types: 
            if cols_by_type.get(key): 
                numeric_cols.extend(cols_by_type.get(key))
        return numeric_cols


    def replace_missing(self, cols, method='mode'):
        ''' Look for all NaN values (nulls, none, blanks) in the input columns and replace
        them according to the method selected. If you define method = 'remove' all the 
        rows with one or more NaN will be deleted from the dataset.
        '''
        # HINT: Be careful with datetime columns, since they use NaT instead of NaN
        
        for col in cols:
            count = self.dataset[col].isna().count()
            if method == 'mode':
                current_mode = self.dataset[col].mode(axis=1, dropna=True)
                self.dataset[col] = self.dataset[col].fillna(current_mode)
            elif method == 'mean':
                current_mean = self.dataset[col].mean(axis=1, dropna=True)
                self.dataset[col] = self.dataset[col].fillna(current_mean)
            elif method == 'median':
                current_median = self.dataset[col].median(axis=1, dropna=True)
                self.dataset[col] = self.dataset[col].fillna(current_median)
            elif method == 'remove':
                self.dataset[col] = self.dataset[col].dropna(axis=1)
            else:
                ValueError('Replace missing values method not implemented.')

            print(f'Warning! {count} rows removed in column {col}')


    def standardize(self, cols, method='z_score'):

        if method == 'z_score':
            for col in cols:
                self.dataset[col] = (self.dataset[col] - self.dataset[col].mean() / self.dataset[col].std())
            self.is_standardize = True            
        elif method == '0-1':
            # self.is_standardize = True
            pass
        else:
            raise ValueError('Standardize method not supported')
            

    # TODO: Implement using SOLID.
    def reduction_dims(self, cols=None, method='pca', final_number_dims=2, visualize=True):
        if not self.is_standardize:
            raise ValueError('You should standardize your columns first.')
        if not cols:
            cols = self.dataset.columns.tolist()

        if method == 'pca':
            pca = PCA(n_components=final_number_dims)
            principal_components = pca.fit_transform(self.dataset[cols])

            for index in range(0, final_number_dims):
                self.dataset[f'PC{index + 1}'] = principal_components[:,index]

            print('Principal components analysis finished. Explained variance ratio:')
            components_variance = ['{:.12f}'.format(i)[:8] for i in pca.explained_variance_ratio_]
            print(components_variance)

            if visualize and final_number_dims == 2:
                x = self.dataset['PC1']
                y = self.dataset['PC2']        
                scalex = 1.0/(x.max() - x.min())
                scaley = 1.0/(y.max() - y.min())
                coeff = np.transpose(pca.components_)

                fig = plt.figure(figsize = (8,8))
                sp = fig.add_subplot(1,1,1) 
                sp.set_xlabel(f'PC 1 - Variance ratio: {components_variance[0]}', fontsize = 15)
                sp.set_ylabel(f'PC 2 - Variance ratio: {components_variance[1]}', fontsize = 15)
                sp.set_xlim(-1,1)
                sp.set_ylim(-1,1)
                sp.set_title('PCA Biplot', fontsize = 20)
                sp.scatter(x * scalex, y * scaley, s = 50)
                for i, col in enumerate(cols):
                    plt.arrow(0, 0, coeff[i,0], coeff[i,1], color = 'r', head_width=0.02, length_includes_head = True)
                    plt.text(coeff[i,0] /2, coeff[i,1] /2, col, color = 'g', ha = 'left', va = 'baseline')
                sp.grid()
                plt.show()


    # TODO: Implement this using SOLID
    def clusterization(self, cols=None, method='k_means', visualize=True, n_clusters=None):

        if not self.is_standardize:
            raise ValueError('You should standardize your columns first.')

        if method == 'k_means':
            print('='*27)
            print('Clustering using K-Means')
            print('='*27)

            kmeans_kwargs  = {
                'init': 'random',
                'n_init': 10,
                'max_iter': 300,
                'random_state': 42,
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
                # plt.style.use('fivethirtyeight')
                plt.plot(range(2, 11), sse)
                plt.xticks(range(2, 11))
                plt.title('K-Means')
                plt.xlabel('Number of Clusters')
                plt.ylabel('SSE')
                plt.show()

                # plt.style.use('fivethirtyeight')
                plt.plot(range(2, 11), kmeans_silhouette_coefficients)
                plt.xticks(range(2, 11))
                plt.title('K-Means')
                plt.xlabel('Number of Clusters')
                plt.ylabel('Silhouette Coefficient')
                plt.show()

            kl = KneeLocator(range(2, 11), sse, curve='convex', direction='decreasing')
                
            number_clusters_best = kl.elbow
            print(f'Best number of clusters using elbow method: {number_clusters_best}')
            print('')
            print(f'See the graph Silhouette coefficient vs number of clusters to define \
                the best amount of clusters in your case. \
                (Silhouette coefficient goes from -1 to 1, near to 1 is better)')
            print('')

        elif method == 'k_medoids':
            print('='*27)
            print('Clustering using K-Medoids')
            print('='*27)

            kmedoids_kwargs  = {
                'metric': 'euclidean',
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
                # plt.style.use('fivethirtyeight')
                plt.plot(range(2, 11), sse)
                plt.xticks(range(2, 11))
                plt.title('K-Medoids')
                plt.xlabel('Number of Clusters')
                plt.ylabel('SSE')
                plt.show()

                # plt.style.use('fivethirtyeight')
                plt.plot(range(2, 11), kmedoids_silhouette_coefficients)
                plt.xticks(range(2, 11))
                plt.title('K-Medoids')
                plt.xlabel('Number of Clusters')
                plt.ylabel('Silhouette Coefficient')
                plt.show()

            kl = KneeLocator(range(2, 11), sse, curve='convex', direction='decreasing')
                
            number_clusters_best = kl.elbow
            print(f'Best number of clusters using elbow method: {number_clusters_best}')
            print('')
            print(f'See the graph Silhouette coefficient vs number of clusters to define \
                the best amount of clusters in your case. \
                (Silhouette coefficient goes from -1 to 1, near to 1 is better)')
            print('')

        elif method == 'dbscan':
            print('='*27)
            print('Clustering using DBScan')
            print('='*27)

            silhouette_eps_ncluster = {}
            for eps in np.linspace(0.1, 4, 10):
                dbscan = DBSCAN(eps=eps)
                dbscan.fit(self.dataset[cols])
                if len(set(dbscan.labels_)) > 1:
                    # Silhouette score requires at least 2 clusters to be calculated.
                    # Rows marked with dbscan.labels_=-1 don't belong to a real cluster
                    # but are considered noise.
                    score = round(silhouette_score(self.dataset[cols], dbscan.labels_), 4)
                    nclusters = len(set(dbscan.labels_))
                    
                    silhouette_eps_ncluster[score] = ((eps, nclusters))

            if visualize:
                y, tup = zip(*silhouette_eps_ncluster.items())
                x = [eps for eps, nclusters in tup]

                # plt.style.use('fivethirtyeight')
                plt.plot(x, y)
                plt.xticks(np.linspace(0.1,4,10))
                plt.title('DBScan')
                plt.xlabel('eps')
                plt.ylabel('Silhouette Coefficient')
                plt.show()

            nclusters_best = silhouette_eps_ncluster.get(max(silhouette_eps_ncluster.keys()), -1)[1]
            print(f'Best number of clusters using Silhouette over multiple eps: {nclusters_best}')
            print('')
        else:
            raise ValueError('Clustering method not implemented.')
        

    def dummy_cols_from_text(self, col, sep=',', n_cols=10):
        if self.dataset[col].dtype == np.number:
            raise ValueError('The origin column to generate dummy columns must be text.')

        dummy_df = self.dataset[col].str.get_dummies(sep=sep)

        top_dummy_df = dummy_df[dummy_df.sum().sort_values(ascending=False, inplace=False)[0:n_cols].index]

        self.dataset = pd.concat([self.dataset, top_dummy_df], axis=1, sort=False)


        
    def reset (self):
        self.__init__(self.path, self.format)

    