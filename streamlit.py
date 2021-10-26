import datetime
import time
import pandas as pd
import streamlit as st
import numpy as np
import os
import requests
import matplotlib.pyplot as plt

BASE_API = os.getenv('API','http://localhost:5000')

st.markdown(
    """
    <style>
    .reportview-container {
        background: #FFFFFF
    }
   .sidebar .sidebar-content {
        background: #FFFFFF
    }
    </style>
    """,
    unsafe_allow_html=True
)

BASE_API = os.getenv('API','http://localhost:5000')
# st.session_state.user_preference = []
if 'user_preference' not in st.session_state:
    st.session_state.user_preference = []

if 'recommendation' not in st.session_state:
    st.session_state.recommendation = False

def find_book(text):
    print('INSIDE CALLBACK ', text)
    res = requests.get(f"{BASE_API}/auto?title={text}")
    st.session_state.titles = res.json()['response']
    return st.session_state.titles

if 'titles' not in st.session_state:
    st.session_state.titles = [' ', *find_book('')]

def send_reviews(data):
    print('INSIDE CALLBACK ', data)
    res = requests.post(f"{BASE_API}/recommender/predict")
    st.session_state.titles = res.json()['response']
    return st.session_state.titles



# título
st.title("The Librarian")

st.header("Datos sobre un pais en concreto")


option = st.selectbox(
     'How would you like to be contacted?',
     (st.session_state.titles))

rate = st.slider('rate this book ', 1,5)


st.write('You selected:', option)

if st.button("Add review"):
    st.session_state.user_preference.append({
        'title': option,
        'rate': rate
    })
    
st.dataframe(data=st.session_state.user_preference)

if st.button("recommend me something!"):
    # send_reviews(st.session_state.user_preference)
    st.session_state.recommendation = True
     

with st.container():
    if st.session_state.recommendation:
        st.write("This is inside the container")

    
