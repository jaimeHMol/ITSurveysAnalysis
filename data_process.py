import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from kneed import KneeLocator

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

        self.path = path
        self.format = format
        self.dataset_raw = dataset
        self.dataset = dataset_raw
        
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
        if all(isinstance(item, int) for item in cols_to_remove):
            self.dataset.drop(self.dataset.columns[cols_to_remove], axis=1)
        else:
            self.dataset.drop(cols_to_remove, axis=1)

    def rename_cols(self, cols_to_rename):
        self.dataset.rename(mapper=cols_to_rename, axis=1)

    def unify_format(self, cols, search_func, transform_func):
        pass

    def standardize(self, cols, method):

        if method == "z-score":
            for col in self.dataset:
                self.dataset[col] = (self.dataset[col] - self.dataset[col].mean() / self.dataset[col].std())
            self.is_standardize = True            
        elif method == "0-1":
            # self.is_standardize = True
            pass
        else:
            raise ValueError("Standardize method not supported")
            
    
    # TODO: Implement using SOLID.
    def reduction_dims(self, cols, method='pca', final_number_dims=2, visualize=True):
        if not is_standardize:
            raise ValueError("You should standardize your columns first.")

        if method == 'pca':
            pca = PCA(n_components=final_number_dims)
            principal_components = pca.fit_transform(self.dataset)

            for index in range(0, final_number_dims):
                self.dataset[f"PC{index + 1}"] = principal_components[:,index]

            print("Principal components analysis finished. Explained variance ratio:"
            print(pca.explained_variance_ratio_)

            if visualize and final_number_dims == 2:
                fig = plt.figure(figsize = (8,8))
                ax = fig.add_subplot(1,1,1) 
                ax.set_xlabel('PC 1', fontsize = 15)
                ax.set_ylabel('PC 2', fontsize = 15)
                ax.set_title('2 component PCA', fontsize = 20)
                ax.scatter(self.datset['PC 1']
                            , self.dataset['PC 2']
                            , s = 50)
                ax.grid()





    # TODO: Implement this using SOLID
    def clusterization(self, method='k_means', visualize=True):

        if method == 'k_means':
            # Clustering - Kmeans (initial approach with 3 clusters)
            kmeans = KMeans(
                init="random",
                n_clusters=3,
                n_init=10,
                max_iter=300,
                random_state=42,
            )
            kmeans.fit(standardized_features)

            # The lowest Sum of Squared Error (SSE) value
            kmeans.inertia_

            # Final locations of the centroid
            kmeans.cluster_centers_

            # The number of iterations required to converge
            kmeans.n_iter_

            # How many clusters should be calculated?
            #   Using elbow method
            print("="*27)
            print("Clustering using K-Means")
            print("="*27)
            kmeans_kwargs  = {
                "init": "random",
                "n_init": 10,
                "max_iter": 300,
                "random_state": 42,
            }

            sse = []
            for k in range(1, 11):
                kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
                kmeans.fit(standardized_features)
                sse.append(kmeans.inertia_)

            if visualize:
                plt.style.use("fivethirtyeight")
                plt.plot(range(1, 11), sse)
                plt.xticks(range(1, 11))
                plt.title("K-Means")
                plt.xlabel("Number of Clusters")
                plt.ylabel("SSE")
                plt.show()

            kl = KneeLocator(
                    range(1, 11), sse, curve="convex", direction="decreasing"
                )
            # Best number of clusters:
            number_clusters_best = kl.elbow
            print(f"Best number of clusters using elbow method: {number_clusters_best}")

            # Silhouette coefficient (goes from -1 to 1, near to 1 is better)
            kmeans_silhouette_coefficients = []
            for k in range(2, 11):
                kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
                kmeans.fit(standardized_features)
                score = silhouette_score(standardized_features, kmeans.labels_)
                kmeans_silhouette_coefficients.append(score)

            if visualize:
                plt.style.use("fivethirtyeight")
                plt.plot(range(2, 11), kmeans_silhouette_coefficients)
                plt.xticks(range(2, 11))
                plt.title("K-Means")
                plt.xlabel("Number of Clusters")
                plt.ylabel("Silhouette Coefficient")
                plt.show()


        elif method == 'k_medoids':
            # Clustering - Kmedoids (initial approach with 3 clusters)
            kmedoids = KMedoids(
                metric="euclidean",
                n_clusters=3,
            )
            kmedoids.fit(standardized_features)

            # The lowest Sum of Squared Error (SSE) value
            kmedoids.inertia_

            # Final locations of the centroid
            kmedoids.cluster_centers_

            # The number of iterations required to converge
            kmedoids.n_iter_

            # How many clusters should be calculated?
            #   Using elbow method
            print("="*27)
            print("Clustering using K-Medoids")
            print("="*27)

            kmedoids_kwargs  = {
                "metric": "euclidean",
            }

            sse = []
            for k in range(1, 11):
                kmedoids = KMedoids(n_clusters=k, **kmedoids_kwargs)
                kmedoids.fit(standardized_features)
                sse.append(kmedoids.inertia_)

            if visualize:
                plt.style.use("fivethirtyeight")
                plt.plot(range(1, 11), sse)
                plt.xticks(range(1, 11))
                plt.title("K-Medoids")
                plt.xlabel("Number of Clusters")
                plt.ylabel("SSE")
                plt.show()

            kl = KneeLocator(
                    range(1, 11), sse, curve="convex", direction="decreasing"
                )
            # Best number of clusters:
            number_clusters_best = kl.elbow
            print(f"Best number of clusters using elbow method: {number_clusters_best}")

            # Silhouette coefficient (goes from -1 to 1, near to 1 is better)
            kmedoids_silhouette_coefficients = []
            for k in range(2, 11):
                kmedoids = KMedoids(n_clusters=k, **kmedoids_kwargs)
                kmedoids.fit(standardized_features)
                score = silhouette_score(standardized_features, kmedoids.labels_)
                kmedoids_silhouette_coefficients.append(score)

            if visualize:
                plt.style.use("fivethirtyeight")
                plt.plot(range(2, 11), kmedoids_silhouette_coefficients)
                plt.xticks(range(2, 11))
                plt.title("K-Medoids")
                plt.xlabel("Number of Clusters")
                plt.ylabel("Silhouette Coefficient")
                plt.show()


        elif method == 'dbscan';
            # Clustering - DBScan
            print("="*27)
            print("Clustering using DBScan")
            print("="*27)
            dbscan = DBSCAN(eps=0.5)

            dbscan.fit(standardized_features)

            # Number of clusters (For the eps used as input parameter)
            len(set(dbscan.labels_))

            dbscan_silhouette = silhouette_score(standardized_features, dbscan.labels_)

            # Finding best number of cluster (Choosing the correct eps)
            dbscan_silhouette_coefficients = []
            for eps in np.linspace(0.1,4,10):
                dbscan = DBSCAN(eps=eps)
                dbscan.fit(standardized_features)
                score = silhouette_score(standardized_features, dbscan.labels_)
                dbscan_silhouette_coefficients.append(score)

            if visualize:
                plt.style.use("fivethirtyeight")
                plt.plot(np.linspace(0.1,4,10), dbscan_silhouette_coefficients)
                plt.xticks(np.linspace(0.1,4,10))
                plt.title("DBScan")
                plt.xlabel("eps")
                plt.ylabel("Silhouette Coefficient")
                plt.show()

            # TODO: Detect this value programatically
            dbscan = DBSCAN(eps=1.8)
            dbscan.fit(standardized_features)

            # Best number of clusters according to the best Silhouette score over multiples eps.
            number_clusters_best = len(set(dbscan.labels_))
            print(f"Best number of clusters using Silhouette over multiple eps: {number_clusters_best}")

        else:
            ValueError("Clustering method not implemented.")
        



    def reset (self):
        __init__(self.path, self.format)

    