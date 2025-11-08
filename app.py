import streamlit as st
import pickle
import pandas as pd
import requests
import time
from typing import List, Optional

# Configure page
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        font-size: 3.5rem; 
        color: #ff6b6b; 
        text-align: center; 
        margin-bottom: 2rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        font-weight: 800;
        letter-spacing: 2px;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Movie Card */
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: white;
        text-align: center;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        cursor: pointer;
    }
    
    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Stats Container */
    .stats-container {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
        transition: transform 0.2s;
    }
    
    .stats-container:hover {
        transform: scale(1.05);
    }
    
    /* Selected Movie Container */
    .selected-movie-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
        margin: 2rem 0;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Filter Info Box */
    .filter-info {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
        color: #fff;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* Section Title */
    .section-title {
        font-size: 2rem;
        color: #667eea;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 700;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        
    }
    
    [data-testid="stSidebar"] * {
        color:#68172c; !important;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Movie Info Box */
    .movie-info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Similarity Badge */
    .similarity-badge {
        background: #ffeb3b;
        color: #333;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-top: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Image Container */
    .img-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    
    .img-container:hover {
        transform: scale(1.05);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 10px;
        padding: 1rem;
        animation: slideIn 0.5s ease-out;
    }
    
    .stError {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 2px solid #667eea;
        font-size: 1rem;
    }
    
    .footer p {
        margin: 0.5rem 0;
    }
    
    /* Selectbox Styling */
    .stSelectbox>div>div {
        background: black;
        border-radius: 8px;
        border: 2px solid #667eea;
    }
    
    /* Slider Styling */
    .stSlider>div>div>div {
        background: #667eea;
    }
    
    /* Checkbox Styling */
    .stCheckbox>label {
        font-weight: 600;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

TMDB_API_KEY = "88f6ea183ab85855cdc99c4d49d77060"

MOOD_GENRE_MAP = {
    "Happy": ["Comedy","Animation","Family","Musical"],
    "Sad": ["Drama","Documentary"],
    "Romantic": ["Romance","Drama"],
    "Action": ["Action","Adventure","Thriller"],
    "Thriller": ["Thriller","Horror","Mystery"]
}

AGE_RATING_MAP = {
    "Kids (0-12)": ["G","PG"],
    "Teens (13-17)": ["PG","PG-13"],
    "Adults (18+)": ["PG-13","R","NC-17"]
}

import requests, pickle, pandas as pd, os

@st.cache_data
def load_data():
    # ✅ Direct Dropbox links (no tokens, no ?dl=0)
    MOVIE_DICT_URL = "https://dl.dropboxusercontent.com/scl/fi/kgrn1642a53ci1two9zc3/movie_dict.pkl"
    SIMILARITY_URL = "https://dl.dropboxusercontent.com/scl/fi/zhalvy3t6bgadt4ea1o3z/similarity.pkl"

    def download_from_url(url, destination):
        """Download binary file directly (Dropbox raw URL)."""
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            st.error(f"❌ Failed to download {os.path.basename(destination)} (HTTP {response.status_code})")
            st.stop()

        with open(destination, "wb") as f:
            for chunk in response.iter_content(8192):
                if chunk:
                    f.write(chunk)

    # Download files only once
    if not os.path.exists("movie_dict.pkl"):
        st.info("📥 Downloading movie_dict.pkl from Dropbox...")
        download_from_url(MOVIE_DICT_URL, "movie_dict.pkl")

    if not os.path.exists("similarity.pkl"):
        st.info("📥 Downloading similarity.pkl from Dropbox...")
        download_from_url(SIMILARITY_URL, "similarity.pkl")

    # Validate file contents (ensure not HTML)
    def validate_pickle(path):
        with open(path, "rb") as f:
            start = f.read(20)
            if start.startswith(b"<") or start.startswith(b"<!"):
                st.error(f"⚠️ File {os.path.basename(path)} looks like HTML, not pickle. Check Dropbox link.")
                st.stop()

    validate_pickle("movie_dict.pkl")
    validate_pickle("similarity.pkl")

    # Load pickled data
    try:
        with open("movie_dict.pkl", "rb") as f:
            movies_dict = pickle.load(f)
        with open("similarity.pkl", "rb") as f:
            similarity = pickle.load(f)
    except Exception as e:
        st.error("❌ Failed to load model files. Verify Dropbox links and file integrity.")
        st.exception(e)
        st.stop()

    movies = pd.DataFrame(movies_dict)
    return movies, similarity




def clean_movie_data(movies):
    # Convert year to number
    if "year" in movies.columns:
        movies["year"] = pd.to_numeric(movies["year"], errors="coerce")
        movies = movies.dropna(subset=["year"])
        movies["year"] = movies["year"].astype(int)

    # Convert genre string → list
    if "genres" in movies.columns:
        movies["genres"] = movies["genres"].apply(
            lambda x: eval(x) if isinstance(x,str) and x.startswith("[") else x
        )
    return movies

@st.cache_data
def get_movie_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    try:
        r = requests.get(url,timeout=5).json()
        poster = r['results'][0].get('poster_path')
        return f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/300x450/667eea/white?text=No+Poster"
    except:
        return "https://via.placeholder.com/300x450/667eea/white?text=No+Poster"

def get_movie_details(title):
    try:
        search = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}").json()
        if not search['results']: return {"error":"Movie not found"}
        movie_id = search['results'][0]['id']
        video = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}").json()
        trailer = next((f"https://www.youtube.com/watch?v={v['key']}" for v in video['results'] if v['type']=="Trailer"), None)
        info = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}").json()
        return {
            "title":info.get("title"), "overview":info.get("overview"),
            "trailer_url":trailer, "release_date":info.get("release_date"),
            "rating":info.get("vote_average"), "runtime":info.get("runtime")
        }
    except:
        return {"error":"API error"}

def recommend(movie, movies, similarity):
    if movie not in movies['title'].values:
        return [("Movie not found",0)]
    idx = movies[movies['title']==movie].index[0]
    distances = similarity[idx]
    movies_list = sorted(list(enumerate(distances)), key=lambda x:x[1], reverse=True)[1:6]
    return [(movies.iloc[i]['title'],score) for i,score in movies_list]

def filter_data(movies,mood,age,genres,year_range):
    df = movies.copy()
    if mood!="All Moods":
        df = df[df['genres'].apply(lambda x:any(g in str(x) for g in MOOD_GENRE_MAP[mood]))]
    if age!="All Ages" and "rating" in df.columns:
        df = df[df['rating'].isin(AGE_RATING_MAP[age])]
    df = df[(df['year']>=year_range[0]) & (df['year']<=year_range[1])]
    if genres:
        df = df[df['genres'].apply(lambda x:any(g in str(x) for g in genres))]
    return df

def main():
    movies, similarity = load_data()
    movies = clean_movie_data(movies)

    all_genres = sorted({g for lst in movies["genres"] for g in lst}) if "genres" in movies else []
    all_years = sorted(movies["year"].unique()) if "year" in movies else [1900,2025]

    st.markdown('<h1 class="main-header">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Filters & Settings")
        
        st.subheader("😊 Mood Selection")
        mood = st.selectbox("Select Your Mood:",["All Moods"]+list(MOOD_GENRE_MAP.keys()))
        
        st.subheader("👥 Age Group")
        age = st.selectbox("Age Group:",["All Ages"]+list(AGE_RATING_MAP.keys()))
        
        st.subheader("🎭 Genre Filter")
        genres = st.multiselect("Select Genre(s):",all_genres)
        
        st.subheader("📅 Year Range")
        min_y,max_y = int(min(all_years)), int(max(all_years))
        year_range = st.slider("Select Year Range:",min_value=min_y, max_value=max_y, value=(min_y,max_y))

        st.subheader("🎨 Display Options")
        show_scores = st.checkbox("Show Similarity %",False)
        show_posters = st.checkbox("Show Posters",True)
        
        st.markdown("---")
        st.info(f"📚 **Total Database:** {len(movies):,} movies")

    filtered = filter_data(movies,mood,age,genres,year_range)

    # Show active filters
    active_filters = []
    if mood != "All Moods":
        active_filters.append(f"Mood: {mood}")
    if age != "All Ages":
        active_filters.append(f"Age: {age}")
    if genres:
        active_filters.append(f"Genres: {', '.join(genres)}")
    
    if active_filters:
        st.markdown(f"""
        <div class="filter-info">
            <strong>🔍 Active Filters:</strong> {' | '.join(active_filters)}<br>
            <strong>📊 Movies Found:</strong> {len(filtered):,}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="stats-container">
            <h3>🎬 Movies Available</h3>
            <h2>{len(filtered):,}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h2 style="text-align:center; color:#667eea;">🎯 Select a Movie</h2>', unsafe_allow_html=True)

    movie_list = sorted(filtered['title'].values) if len(filtered) else ["No movie"]

    col1, col2 = st.columns([3, 1])
    with col1:
        movie = st.selectbox("Choose a movie to get recommendations:", movie_list, label_visibility="collapsed")
    with col2:
        btn = st.button("🚀 Get Recommendations", type="primary", use_container_width=True, disabled=(movie=="No movie"))

    if btn and movie != "No movie":
        with st.spinner("🔍 Finding similar movies..."):
            time.sleep(0.3)
            recs = recommend(movie,movies,similarity)

        if recs[0][0] != "Movie not found":
            st.success("✅ Found great recommendations for you!")
            
            # Selected Movie Display
            st.markdown(f"""
            <div class="selected-movie-container">
                <h2>🎯 Selected Movie</h2>
                <h1 style="font-size:2.5rem; margin:1rem 0;">{movie}</h1>
                <p style="font-size:1.1rem;">Discover similar movies based on your preferences below</p>
            </div>
            """, unsafe_allow_html=True)

            # Movie Details
            details = get_movie_details(movie)
            if "error" not in details:
                st.markdown("---")
                st.markdown('<div class="section-title">📹 Movie Information</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"""
                    <div class="movie-info-box">
                        <h4>⭐ Rating</h4>
                        <h2>{details['rating']}/10</h2>
                        <hr style="margin:1rem 0; border-color:rgba(255,255,255,0.3);">
                        <p><strong>📅 Release:</strong> {details['release_date']}</p>
                        <p><strong>🎞️ Runtime:</strong> {details['runtime']} mins</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="movie-info-box">
                        <h4>📖 Overview</h4>
                        <p style="line-height:1.6; margin-top:1rem;">{details['overview']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Trailer
                if details['trailer_url']:
                    st.markdown("---")
                    st.markdown('<div class="section-title">▶️ Watch Trailer</div>', unsafe_allow_html=True)
                    st.video(details['trailer_url'])
                else:
                    st.warning("⚠️ Trailer not available for this movie")

            # Recommendations
            st.markdown("---")
            st.markdown('<div class="section-title">📽️ Similar Movies You Might Like</div>', unsafe_allow_html=True)
            
            cols = st.columns(5)
            for c,(title,score) in zip(cols,recs):
                with c:
                    if show_posters:
                        poster = get_movie_poster(title)
                        st.markdown('<div class="img-container">', unsafe_allow_html=True)
                        st.image(poster, use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    score_html = f'<div class="similarity-badge">Match: {score:.1%}</div>' if show_scores else ''
                    st.markdown(f"""
                    <div class="movie-card">
                        <strong style="font-size:1.1rem;">{title}</strong>
                        {score_html}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("❌ Movie not found in our database. Please try another movie.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p style="font-size:1.2rem; font-weight:600;">🚀 Built with ❤️ using Python, Streamlit & Machine Learning</p>
        <p>😊 Mood-Based Filtering • 👥 Age-Appropriate Content • 🤖 Cosine Similarity • 📊 Data Science</p>
        <p style="margin-top:1rem; color:#667eea;">© 2024 Movie Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

if __name__=="__main__":
    main()