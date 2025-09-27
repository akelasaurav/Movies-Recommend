import streamlit as st
import pandas as pd
import pickle
import requests
import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movie_dict = pickle.load(open(os.path.join(BASE_DIR, 'movie_dic.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))



import time

def fetch_poster(movie_id, retries=3):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d63b1d2a6f3dada2f764855c95172d54&language=en-US'
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if not poster_path:
                return None
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(1)
    return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster = []
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

# movie_dict= pickle.load(open('movie_dic.pkl','rb'))
# movies = pd.DataFrame(movie_dict)
#
# similarity= pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')

select_movie_name = st.selectbox(
    "How would you like to movie recommendation? ",
     movies['title'].values )

if st.button("Recommend"):
    names,poster =recommend(select_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])

