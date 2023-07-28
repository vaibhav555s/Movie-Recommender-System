import streamlit as st
import pickle
import pandas as pd
import requests

def recommend(movie):
    movie_index = movie_list[movie_list["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse = True, key = lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    
    for i in movies:

        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movies.append(movie_list.iloc[i[0]].title)

        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f5d6a2625aaf7b6b2a791a6731ee24b2&language=en-us")
    data = response.json()
    path = "http://image.tmdb.org/t/p/w500/" + data["poster_path"]
    return path

movie_dict = pickle.load(open("movies_dict.pkl", "rb"))
movie_list = pd.DataFrame(movie_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


#Webpage Code
st.title("Movie Recommender")

selected_movie_name = st.selectbox("Select a movie", movie_list["title"].values)


if st.button('Recommend Similar Movies'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])