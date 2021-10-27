import datetime
import time
import pandas as pd
import streamlit as st
import numpy as np
import os
import requests
import matplotlib.pyplot as plt
import json

BASE_API = os.getenv('API','http://localhost:5000')

st.markdown(
    """
    <style>
    .reportview-container {
        background: #FFFFFF;
    }
   .sidebar .sidebar-content {
        background: #FFFFFF
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content:space-between}</style>', unsafe_allow_html=True)


BASE_API = os.getenv('API','http://localhost:5000')

model_types = {
    "General": "optimal_k_down", 
    "Equilibrado (Optimo)": "optimal_k", 
    "Especifico": "optimal_k_up"
}

if 'user_preference' not in st.session_state:
    st.session_state.user_preference = []

if 'recommendation' not in st.session_state:
    st.session_state.recommendation = False

if 'titles' not in st.session_state:
    st.session_state.recommendation = []

if 'recommended_books' not in st.session_state:
    st.session_state.recommended_books = []

def find_book(text):
    res = requests.get(f"{BASE_API}/auto?title={text}")
    st.session_state.titles = res.json()['response']
    return st.session_state.titles

if 'titles' not in st.session_state:
    st.session_state.titles = [' ', *find_book('')]

def send_reviews(data, model):
    header = {"content-type": "application/json"}
    res = requests.post(
        f"{BASE_API}/recommender/predict",
        json.dumps({
            "user": data,
            "model": model
        }),
        headers=header
    )
    st.session_state.recommended_books = res.json()['response']
    return st.session_state.recommended_books


# título
# st.title("The Librarian")
st.image("./src/images/lib.png",use_column_width='auto')
st.header("Recomendador de libros")


model = st.radio(
     "Elije que  tipo  de modelo  prefieres",
     ('General', 'Equilibrado (Optimo)', 'Especifico'))


option = st.selectbox(
     'Comoo puntuarias a este libro?',
     (st.session_state.titles))

rate = st.slider('puntuacion', 1,5)

st.write('You selected:', option)

if st.button("Puntuar"):
    st.session_state.user_preference.append({
        "title": option,
        "rate": rate
    })
    
st.dataframe(data=st.session_state.user_preference)

if st.button("Hazme una recomendacion!"):
    with st.spinner('Wait for it...'):
        send_reviews(st.session_state.user_preference, model_types[model])
        st.session_state.recommendation = True

     

with st.container():
    if st.session_state.recommendation:
        books = st.session_state.recommended_books

        numbers  = [0,1,2,3]
        n = numbers[0]

        st.balloons()
        
        cols = st.columns(4)
        for book in books['cluster_list']:
            title = book['title']
            cols[n].markdown(f'<p class="big-font">{title}</p>', unsafe_allow_html=True)
            cols[n].image(book['image_url'],caption=book['authors'],use_column_width='auto')
            n = n+1
            if n>3:
                n = numbers[0]


    
