import streamlit as st
st.title('Movie Recommendation System')
import pickle
import pandas as pd
import requests
# requests for api calling
movies=pickle.load(open('movies.pkl','rb'))
movies_titles=movies['title'].values
similarity=pickle.load(open('similarity.pkl','rb'))
def fetch_poster(movie_id):
    # not able to login in tmdb movie site from there we will fetch
    # the api key and put it here and the api will get hit
    response=requests.get("https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id=movie_id))
    data =response.json()
    return "https://image.tmdb.org/t/p/{size}/" + data['poster_path']


def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    # distance array h
    movies_distances = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_distances:
        movie_id=movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

selected_movie_name=st.selectbox('Select Movie to recommend',movies_titles)
if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    # now for displaying that poster and movie name
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])


    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])

