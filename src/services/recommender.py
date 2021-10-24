import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pickle


class Reccomender():

    def __init__(self):
        self.model = None


    def clustering(self, x, n):
        """Método encargado de realizar clustering de usuarios
        """
        
        kmeans_model = KMeans(n_clusters=n,init = 'k-means++', n_init = 20)
        x_columns = x.columns[1:]
        x_train = preprocessing.Normalizer().fit_transform(x[x_columns])

        self.kmeans = kmeans_model
        self.kmeans.fit(x_train)

        self.centroids = pd.DataFrame(self.kmeans.cluster_centers_, columns=x_columns)
        
        x.index.name = 'user_uuid'
        y = pd.Series(self.kmeans.labels_, name='Cluster')
        
        return x, y


    def model_train(self, x, y):
        """Método encargado de realizar el entrenamiento del modelo
        """
        # Se realizan pruebas con varios valores de k para obtener el mejor modelo posible
        self.model.fit(x, y)


    def save_reccomender(self, path, model_name):
        """Método encargado de realizar el guardado del recomendador
        """
        with open(os.path.join(path, model_name), 'wb') as file:
            pickle.dump(self, file)



    def train_reccomender(self, clean_data, path, model_name):
        """Método encargado de realizar el entrenamiento completo del recomendador

        Parameters
        ----------
        clean_data : pd.Dataframe
            Datos sobre los que realizar el entrenamiento
        path : str
            String con la ruta local de guardado previo a la subida a GCS del recomendador
        model_name: str
            String con el nombre del modelo
        
        Returns
        -------
        """
        # clean_data = preprocess(raw_data)
        self.trained_columns = clean_data.columns
        
        x, y = self.clustering(clean_data)
        
        self.knn_train(x, y)
        self.save_reccomender(path, model_name)


    def load_model(self, path, model_name):
        """Método encargado de realizar la carga del recomendador desde GCS

        Parameters
        ----------
        path : str
            String con la ruta local de carga posterior a la descarga de GCS del recomendador
        model_name: str
            String con el nombre del modelo
        
        Returns
        -------
        """        
        load_model_gcs(path, model_name, bucket_name='save_pickle_model')
        
        with open(os.path.join(path, model_name), 'rb') as file:
            self.loaded_model = pickle.load(file)


    def predict(self, x):
        """Método encargado de realizar la predicción de un nuevo usuario al cluster asignado

        Parameters
        ----------
        x : pd.Dataframe
            Datos sobre los que realizar la predicción
        
        Returns
        -------
        y : pd.Dataframe
            Dataframe con la probabilidad de pertenencia del nuevo usuario a cada cluster
            y el cluster asignado
        """       
        probabilities = pd.DataFrame(self.model.predict_proba(x))
        asigned_cluster = pd.Series(self.model.predict(x), name='cluster_prediction')

        prediction = pd.concat([probabilities, asigned_cluster], axis=1)

        return prediction
