import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pickle


class Reccomender():

    def __init__(self):
        self.models = {}
        self.users_cluster = {}


    def clustering(self, x, n, users,name_model):
        """
        Método encargado de realizar clustering de usuarios
        """
        
        kmeans_model = KMeans(n_clusters=n,init = 'k-means++', n_init = 20)
        kmeans_model.fit(x)
        self.users_cluster[name_model]  = pd.concat([users,pd.Series(kmeans_model.labels_, name='cluster')], axis=1)
        return kmeans_model


    def model_train(self, x, n_model):
        """
        Método encargado de realizar el entrenamiento del modelo
        """
        self.model[n_model].fit(x)


    def save_reccomender(self, path, model_name):
        """
        Método encargado de realizar el guardado del recomendador
        """
        with open(os.path.join(path, model_name), 'wb') as file:
            pickle.dump(self, file)


    def load_model(self, path, model_name):
        """
        Método encargado de realizar la carga del recomendador
        """

        with open(os.path.join(path, model_name), 'rb') as file:
            self.models = pickle.load(file)

