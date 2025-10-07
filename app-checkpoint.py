import streamlit as st
import pandas as pd

# Load your data
@st.cache_data
def load_data():
    movies = pd.read_csv('movies.csv')
    ratings = pd.read_csv('ratings.csv')
    # Merge movies and ratings for basic recommendations by popularity
    data = pd.merge(movies, ratings, on='movieId')
    return movies, ratings, data

movies, ratings, data = load_data()

st.title("Movie Recommendation System")

# Option 1: Recommend most popular movies based on number of ratings
if st.button("Show Top-Rated Movies Overall"):
    movie_stats = data.groupby('title')['rating'].agg(['mean', 'count']).reset_index()
    popular = movie_stats.sort_values(['count', 'mean'], ascending=[False, False]).head(10)
    st.subheader("Most Popular Movies (by ratings count):")
    st.table(popular[['title', 'mean', 'count']].round(2))

# Option 2: User-based input (if ratings.csv contains userId)
user_ids = ratings['userId'].unique()
user_id = st.selectbox("Select User ID to Get Personalized Recommendations", user_ids)

def recommend_for_user(user_id, data):
    user_ratings = data[data['userId'] == user_id].sort_values('rating', ascending=False)
    return user_ratings[['title', 'rating']].head(10)

if st.button("Recommend for Selected User"):
    recs = recommend_for_user(user_id, data)
    st.subheader(f"Top Recommendations for User {user_id}:")
    st.table(recs)

# Option 3: Search for a movie title (content-based)
movie_titles = movies['title'].unique()
search_title = st.selectbox("Search for movies similar to:", movie_titles)

def recommend_similar(title, movies, n=5):
    # Recommend movies with similar keywords (simple genre/title substring match)
    keywords = title.split()
    mask = movies['title'].str.contains('|'.join(keywords), case=False)
    similar = movies[mask].head(n)
    return similar[['title']]

if st.button("Show Similar Movies"):
    sim = recommend_similar(search_title, movies)
    st.subheader(f"Movies Similar to '{search_title}':")
    st.table(sim)

st.markdown("""
---
**Instructions:**  
- Upload `movies.csv` and `ratings.csv` in the app folder.
- Click respective buttons for recommendations.
- Deploy on Streamlit Cloud for sharing.
""")
