import streamlit as st
import pickle 
import pandas as pd
import requests

import os
import gdown

# Download movies.pkl
if not os.path.exists("movies.pkl"):
    gdown.download(
        "https://drive.google.com/uc?id=1TMi5I7Kgx7efcyle6yQlQMmle08RVfpN",
        "movies.pkl",
        quiet=False
    )

# Download similarity.pkl
if not os.path.exists("similarity.pkl"):
    gdown.download(
        "https://drive.google.com/uc?id=1t0MvF7IIrL5Fh4viwCTuz3iRHU6LIhPJ",
        "similarity.pkl",
        quiet=False
    )

# page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for modern buttons with animation
def create_watch_button(movie_name):
    url = get_youtube_trailer_url(movie_name)
    return f'<a href="{url}" target="_blank" class="watch-btn">▶ Watch</a>'

## fetch poster function
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7f7a3cbd77e28e2d2badf830dfce7f1b'.format(movie_id)
    )
    data = response.json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


## fetch movie details
def fetch_movie_details(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7f7a3cbd77e28e2d2badf830dfce7f1b'.format(movie_id)
    )
    data = response.json()
    
    details = {
        'rating': data.get('vote_average', 'N/A'),
        'release_date': data.get('release_date', 'N/A'),
        'genres': ', '.join([genre['name'] for genre in data.get('genres', [])]),
        'overview': data.get('overview', 'No overview available'),
        'runtime': data.get('runtime', 'N/A')
    }
    return details


## function to get youtube trailer link
def get_youtube_trailer_url(movie_name):
    search_query = movie_name.replace(" ", "+") + "+trailer"
    return f"https://www.youtube.com/results?search_query={search_query}"


## function to create custom button HTML
def create_watch_button(movie_name):
    url = get_youtube_trailer_url(movie_name)
    return f'<a href="{url}" target="_blank" class="watch-btn">▶️ Watch Now</a>'


movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl","rb"))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    similarity_scores = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
        similarity_scores.append(round(i[1] * 100, 2))  # Convert to percentage
        
    return recommended_movies, recommended_movies_poster, similarity_scores


# UI
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Find your next favorite movie 🍿</p>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    '🎥 Select a movie',
    movies['title'].values,
    index=None,
    placeholder="Search and select a movie..."
)

col1, col2 = st.columns([1,5])

with col1:
    recommend_btn = st.button("✨ Recommend")

if recommend_btn:
    
    if selected_movie_name is None:
        st.warning("⚠️ Please select a movie first")
    
    else:
        with st.spinner("⏳ Fetching recommendations..."):
            names, posters, _ = recommend(selected_movie_name)

        # Display selected movie info
        st.markdown("---")
        st.markdown("### 🎬 You Selected")
        
        selected_movie_data = movies[movies['title'] == selected_movie_name].iloc[0]
        selected_poster = fetch_poster(selected_movie_data['movie_id'])
        selected_details = fetch_movie_details(selected_movie_data['movie_id'])
        
        sel_col1, sel_col2 = st.columns([1, 2])
        with sel_col1:
            st.image(selected_poster, width=150)
        
        with sel_col2:
            st.markdown(f"#### {selected_movie_name}")
            st.markdown(f"⭐ **Rating:** {selected_details['rating']}/10")
            st.markdown(f"📅 **Release Date:** {selected_details['release_date']}")
            st.markdown(f"⏱️ **Runtime:** {selected_details['runtime']} mins")
            if selected_details['genres']:
                st.markdown(f"🎭 **Genres:** {selected_details['genres']}")

        st.markdown("---")
        st.markdown("## 🔥 Top 5 Recommendations")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.image(posters[0])
            st.caption(names[0])
            st.markdown(create_watch_button(names[0]), unsafe_allow_html=True)

        with col2:
            st.image(posters[1])
            st.caption(names[1])
            st.markdown(create_watch_button(names[1]), unsafe_allow_html=True)

        with col3:
            st.image(posters[2])
            st.caption(names[2])
            st.markdown(create_watch_button(names[2]), unsafe_allow_html=True)

        with col4:
            st.image(posters[3])
            st.caption(names[3])
            st.markdown(create_watch_button(names[3]), unsafe_allow_html=True)

        with col5:
            st.image(posters[4])
            st.caption(names[4])
            st.markdown(create_watch_button(names[4]), unsafe_allow_html=True)