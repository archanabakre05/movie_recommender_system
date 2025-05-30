import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxOTRiMGY1MjA1YjZmZjA0YTg5NzlhZGJhMzM4YjcxNiIsIm5iZiI6MTc0ODU0NTUwOS43OTEwMDAxLCJzdWIiOiI2ODM4YWZlNTA3OWE0MmUyODcwMzg5MDQiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.hqed_SbhfKTIke9ZbOGmW3-AmdDvY7pKN_yLbRFCQsI"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    poster_path = data.get('poster_path')

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return None
    



def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies=[]
    recommend_movies_posters=[]

    for i in movies_list:
       movie_id = movies.iloc[i[0]].movie_id
       #fetch poster from API
       recommend_movies.append(movies.iloc[i[0]].title)
       recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters



movies_dict= pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button('Recommend'):
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