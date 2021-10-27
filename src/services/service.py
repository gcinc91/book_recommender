
from sqlalchemy.engine.base import Engine
from ..recommender import Reccomender
from ..database import db
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
import numpy as np
import os
import random
from ..utils.jsonfy import jsonfy
from ..utils.mapper_objs import mapper_object_list
import redis
from ..utils.categories import categories


def charge_models():

    recommender  = Reccomender()

    query = f"""
        SELECT * FROM train
    """
    result = list(db.execute(query))

    users_preference = []

    for i  in result:
        users_preference.append(
            {'user_id': i[0],
            'science_fiction': i[1],
            'adventures': i[2],
            'drama': i[3],
            'history': i[4],
            'infantile': i[5],
            'juvenile': i[6],
            'humor': i[7],
            'woman': i[8],
            'thriller': i[9],
            'horror': i[10],
            'love': i[11],
            'suspense': i[12],
            'other': i[13]}
        )
    
    train_df = pd.DataFrame(users_preference)

    X = preprocessing.Normalizer().fit_transform(train_df[train_df.columns[1:]])

    sum_of_squares = []
    k_values = np.arange(5,20)
    for k in k_values:
        kmeans_model = KMeans(n_clusters=k,init = 'k-means++', n_init = 20)
        kmeans_model.fit(X)
        sum_of_squares.append(kmeans_model.inertia_)
    optimal_k = np.arange(5,20)[sum_of_squares < np.mean(sum_of_squares)].min()


    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, '../models')

    print('optimal_k', optimal_k)
    print('path', path)

    recommender.models['optimal_k_down'] = recommender.clustering(X,optimal_k-3, train_df[train_df.columns[:1]],'optimal_k_down')
    recommender.models['optimal_k'] = recommender.clustering(X,optimal_k, train_df[train_df.columns[:1]],'optimal_k')
    recommender.models['optimal_k_up'] = recommender.clustering(X,optimal_k+3, train_df[train_df.columns[:1]],'optimal_k_up')

    print('va a guardar...')
    recommender.save_reccomender(path,'reco_model.pkl')

    return  {
        'optimal_k_down': f"{(optimal_k.astype(int))-3}",
        'optimal_k': f"{(optimal_k.astype(int))}",
        'optimal_k_up': f"{(optimal_k.astype(int))+3}"
    }


def make_recommendation(user, n_model):

    user = transform_user(user)

    recommender  = Reccomender()

    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, '../models/')

    print('CONTROL - CARGANDO MODELO')

    recommender.load_model(path,'reco_model.pkl')
    user_df = pd.DataFrame([user]).reset_index(drop = True)

    print('CONTROL - NORMALIZANDO')

    X = preprocessing.Normalizer().fit_transform(user_df)

    print('CONTROL - PREDICIENDO')

    cluster = recommender.models.models[n_model].predict(X)

    print('CONTROL - CLUSTERS DE ENTRENAMIENTO')

    users_cluster = recommender.models.users_cluster[n_model]
    user_id_list = users_cluster[users_cluster['cluster'] == cluster[0]]['user_id'].values.tolist()

    print('CONTROL - RATINGS')

    sampled_list_users = random.sample(user_id_list, 50)

    query = f"""
        select DISTINCT book_id from ratings where user_id IN {tuple(sampled_list_users)} and rating >= 5 
    """
    books = list(db.execute(query))
    result = [list(b) for b in books]
    flat_list = [item for sublist in result for item in sublist]
    

    sampled_list_books = random.sample(flat_list, 50)

    query = f"""
        select * from books where book_id IN {tuple(sampled_list_books)}
    """
    
    res = list(db.execute(query))

    return {
        "cluster": int(cluster),
        "cluster_list": mapper_object_list(jsonfy(res[:24]))
        }


def  load_titles():

    query = f"""
        select book_id, title from books
    """
    books = list(db.execute(query))

    r = redis.Redis(host='localhost', port=6379, db=0)
    for row in books:
        book_id, title = row
        r.set(title.lower(), book_id)

    return 'Data inserted'

def autocomplete(text):

    r = redis.Redis(host='localhost', port=6379, db=0)
    keys = r.keys(f"*{text.lower()}*")
    
    res = []
    for k in keys:
        res.append(k.decode('utf-8'))

    return list(res)

def transform_user(user):

    user_categories = categories.copy()
    books_ids = []
    titles_list = []
    rates_list = []

    for b in user:
        title, rate = b['title'], b['rate']

        if title not in titles_list:
            books_ids.append(search_book(title))
            titles_list.append(title)
            rates_list.append(rate)

    query = f"""
        select f_categories from books where book_id  IN {tuple(books_ids)}
    """
    books_c = list(db.execute(query))
    books_categories = []

    for cat in books_c:
        for c in cat:   
            if c:   
                c = c.replace('{','')
                c = c.replace('}','')
                l = c.split(',')
                books_categories.append(l)
            books_categories.append(['other'])

    index = 0
    for r in rates_list:
        rate = r
        for cat in books_categories[index]:
            if cat == 'other':
                user_categories[cat] = user_categories[cat]+rate
                break
            user_categories[cat] = user_categories[cat]+rate
        index = index+1

    return user_categories

def search_book(title):
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.get(title).decode('utf-8')
