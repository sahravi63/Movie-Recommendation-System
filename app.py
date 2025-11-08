import streamlit as st
import pickle
import pandas as pd
import requests
import time
from typing import List, Optional

# Configure page
st.set_page_config(
    page_title="CineMatch - AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Modern CSS with Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles effect */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Main Header with Glow Effect */
    .main-header {
        font-size: 4.5rem; 
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center; 
        margin: 2rem 0;
        font-weight: 900;
        letter-spacing: 3px;
        animation: gradientText 5s ease infinite, fadeInDown 1s ease-out;
        text-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
        position: relative;
    }
    
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #a8b2d1;
        margin-top: -1rem;
        margin-bottom: 2rem;
        animation: fadeIn 1.5s ease-out;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Glass Morphism Movie Cards */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        color: white;
        text-align: center;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: 0.5s;
    }
    
    .movie-card:hover::before {
        left: 100%;
    }
    
    .movie-card:hover {
        transform: translateY(-12px) scale(1.05);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.4),
                    0 0 30px rgba(255, 107, 107, 0.3);
        border: 1px solid rgba(255, 107, 107, 0.5);
    }
    
    /* Neon Stats Container */
    .stats-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37),
                    inset 0 0 20px rgba(255, 107, 107, 0.1);
        border: 2px solid rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
        animation: pulseGlow 3s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 20px rgba(255, 107, 107, 0.3); }
        50% { box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 40px rgba(255, 107, 107, 0.6); }
    }
    
    .stats-container:hover {
        transform: scale(1.08) rotate(-2deg);
        border-color: rgba(255, 107, 107, 0.6);
    }
    
    /* Hero Selected Movie */
    .selected-movie-container {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(254, 202, 87, 0.2) 100%);
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 60px rgba(255, 107, 107, 0.3),
                    inset 0 0 50px rgba(255, 255, 255, 0.05);
        margin: 2rem 0;
        animation: scaleIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .selected-movie-container::after {
        content: '🎬';
        position: absolute;
        font-size: 15rem;
        opacity: 0.05;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-15deg);
        pointer-events: none;
    }
    
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Filter Info with Icon */
    .filter-info {
        background: rgba(33, 150, 243, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
        color: #fff;
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.2);
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Section Titles with Underline Animation */
    .section-title {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 3rem 0 1.5rem 0;
        font-weight: 800;
        text-align: center;
        position: relative;
        animation: fadeIn 1s ease-out;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #feca57);
        border-radius: 2px;
        animation: expandWidth 1s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 100px; }
    }
    
    /* Sidebar with Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(48, 43, 99, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(255, 107, 107, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #ff6b6b !important;
        font-weight: 700;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #feca57 !important;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Premium Button */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-size: 1.2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        letter-spacing: 1px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6),
                    0 0 30px rgba(254, 202, 87, 0.4);
    }
    
    /* Info Box with Gradient Border */
    .movie-info-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .movie-info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        z-index: -1;
    }
    
    .movie-info-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.4);
    }
    
    /* Animated Similarity Badge */
    .similarity-badge {
        background: linear-gradient(135deg, #feca57, #ff6b6b);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        margin-top: 0.8rem;
        box-shadow: 0 4px 15px rgba(254, 202, 87, 0.4);
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    /* Image Container with Hover Effect */
    .img-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        transition: all 0.4s ease;
        position: relative;
    }
    
    .img-container::after {
        content: '▶️';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .img-container:hover::after {
        opacity: 0.9;
    }
    
    .img-container:hover {
        transform: scale(1.08) rotate(2deg);
        box-shadow: 0 20px 50px rgba(255, 107, 107, 0.5);
    }
    
    /* Success/Error with Icons */
    .stSuccess {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.2) 0%, rgba(56, 239, 125, 0.2) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 5px solid #38ef7d;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(235, 51, 73, 0.2) 0%, rgba(244, 92, 67, 0.2) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 5px solid #f45c43;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(254, 202, 87, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 5px solid #feca57;
    }
    
    /* Footer with Gradient */
    .footer {
        text-align: center;
        color: #a8b2d1;
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-top: 2px solid rgba(255, 107, 107, 0.3);
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border-radius: 20px 20px 0 0;
    }
    
    .footer p {
        margin: 0.8rem 0;
        line-height: 1.8;
    }
    
    /* Custom Selectbox */
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid rgba(255, 107, 107, 0.3);
        color: white;
        transition: all 0.3s ease;
    }
    
    .stSelectbox>div>div:hover {
        border-color: rgba(255, 107, 107, 0.6);
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
    }
    
    /* Slider with Glow */
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #ff6b6b, #feca57);
    }
    
    .stSlider>div>div>div>div {
        background: white;
        box-shadow: 0 0 15px rgba(255, 107, 107, 0.6);
    }
    
    /* Checkbox Style */
    .stCheckbox>label {
        font-weight: 600;
        color: #e0e0e0 !important;
    }
    
    /* Divider with Gradient */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 107, 0.6), transparent);
        margin: 3rem 0;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-color: #ff6b6b transparent transparent transparent !important;
    }
    
    /* Info Badge */
    .info-badge {
        display: inline-block;
        background: rgba(72, 219, 251, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(72, 219, 251, 0.5);
        color: #48dbfb;
        font-weight: 600;
        margin: 0.5rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Multiselect Pills */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        border-radius: 15px;
        padding: 0.3rem 0.8rem;
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

@st.cache_data
def load_data():
    """Load model files directly from local repository (GitHub-deployed)."""
    try:
        with open("movie_dict.pkl", "rb") as f:
            movies_dict = pickle.load(f)
        with open("similarity.pkl", "rb") as f:
            similarity = pickle.load(f)
        movies = pd.DataFrame(movies_dict)
        return movies, similarity
    except FileNotFoundError as e:
        st.error("❌ Model files not found in the app directory. Please ensure movie_dict.pkl and similarity.pkl exist in your repo.")
        st.exception(e)
        st.stop()
    except Exception as e:
        st.error("❌ Failed to load model files. The files might be corrupted or incompatible.")
        st.exception(e)
        st.stop()

def clean_movie_data(movies):
    if "year" in movies.columns:
        movies["year"] = pd.to_numeric(movies["year"], errors="coerce")
        movies = movies.dropna(subset=["year"])
        movies["year"] = movies["year"].astype(int)
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
        return f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/300x450/302b63/white?text=No+Poster"
    except:
        return "https://via.placeholder.com/300x450/302b63/white?text=No+Poster"

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

    # Hero Header
    st.markdown('''
    <h1 class="main-header">🎬 CINEMATCH</h1>
    <p class="subtitle">✨ Discover Your Next Favorite Movie with AI-Powered Recommendations ✨</p>
    ''', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<h2 style="text-align:center;">⚙️ Customize</h2>', unsafe_allow_html=True)
        
        st.markdown('<h3>😊 Mood Selector</h3>', unsafe_allow_html=True)
        mood = st.selectbox("How are you feeling?",["All Moods"]+list(MOOD_GENRE_MAP.keys()), label_visibility="collapsed")
        
        st.markdown('<h3>👥 Age Filter</h3>', unsafe_allow_html=True)
        age = st.selectbox("Watching with:",["All Ages"]+list(AGE_RATING_MAP.keys()), label_visibility="collapsed")
        
        st.markdown('<h3>🎭 Genre Preferences</h3>', unsafe_allow_html=True)
        genres = st.multiselect("Pick your favorites:",all_genres)
        
        st.markdown('<h3>📅 Time Period</h3>', unsafe_allow_html=True)
        min_y,max_y = int(min(all_years)), int(max(all_years))
        year_range = st.slider("Release years:",min_value=min_y, max_value=max_y, value=(min_y,max_y))

        st.markdown('<h3>🎨 Display Settings</h3>', unsafe_allow_html=True)
        show_scores = st.checkbox("Show Match %",False)
        show_posters = st.checkbox("Show Posters",True)
        
        st.markdown("---")
        st.markdown(f'<div class="info-badge">📚 {len(movies):,} Movies in Database</div>', unsafe_allow_html=True)

    filtered = filter_data(movies,mood,age,genres,year_range)

    # Show active filters
    active_filters = []
    if mood != "All Moods":
        active_filters.append(f"🎭 {mood}")
    if age != "All Ages":
        active_filters.append(f"👥 {age}")
    if genres:
        active_filters.append(f"🎬 {', '.join(genres)}")
    
    if active_filters:
        st.markdown(f"""
        <div class="filter-info">
            <strong style="font-size:1.1rem;">🔍 Active Filters:</strong><br>
            <span style="font-size:1.05rem;">{' • '.join(active_filters)}</span><br><br>
            <strong style="font-size:1.3rem; color:#48dbfb;">📊 {len(filtered):,} Movies Found</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="stats-container">
            <h3 style="margin:0; font-size:1.3rem;">🎬 Available Movies</h3>
            <h2 style="margin:0.5rem 0; font-size:3rem; font-weight:900;">{len(filtered):,}</h2>
            <p style="margin:0; opacity:0.8;">Ready to explore!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h2 class="section-title">🎯 Choose Your Movie</h2>', unsafe_allow_html=True)

    movie_list = sorted(filtered['title'].values) if len(filtered) else ["No movie"]

    col1, col2 = st.columns([3, 1])
    with col1:
        movie = st.selectbox("Select a movie:", movie_list, label_visibility="collapsed")
    with col2:
        btn = st.button("🚀 Find Matches", type="primary", use_container_width=True, disabled=(movie=="No movie"))

    if btn and movie != "No movie":
        with st.spinner("🔮 AI is analyzing... Finding your perfect matches..."):
            time.sleep(0.5)
            recs = recommend(movie,movies,similarity)

        if recs[0][0] != "Movie not found":
            st.success("🎉 Eureka! We found amazing recommendations tailored just for you!")
            
            # Selected Movie Display
            st.markdown(f"""
            <div class="selected-movie-container">
                <h2 style="font-size:1.5rem; margin:0; opacity:0.9;">🎯 You Selected</h2>
                <h1 style="font-size:3.5rem; margin:1.5rem 0; font-weight:900; letter-spacing:2px;">{movie}</h1>
                <p style="font-size:1.2rem; opacity:0.9;">🤖 AI has analyzed thousands of movies to find your perfect matches</p>
            </div>
            """, unsafe_allow_html=True)

            # Movie Details
            details = get_movie_details(movie)
            if "error" not in details:
                st.markdown("---")
                st.markdown('<div class="section-title">📽️ Movie Insights</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"""
                    <div class="movie-info-box">
                        <h4 style="font-size:1.1rem; opacity:0.8; margin-bottom:1rem;">⭐ AUDIENCE RATING</h4>
                        <h2 style="font-size:3rem; margin:0.5rem 0; font-weight:900;">{details['rating']}<span style="font-size:1.5rem; opacity:0.7;">/10</span></h2>
                        <hr style="margin:1.5rem 0; border:none; height:1px; background:rgba(255,255,255,0.2);">
                        <p style="font-size:1.1rem; margin:0.8rem 0;"><strong>📅 Released:</strong> {details['release_date']}</p>
                        <p style="font-size:1.1rem; margin:0.8rem 0;"><strong>⏱️ Duration:</strong> {details['runtime']} minutes</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="movie-info-box">
                        <h4 style="font-size:1.1rem; opacity:0.8; margin-bottom:1rem;">📖 STORYLINE</h4>
                        <p style="line-height:1.8; margin-top:1rem; font-size:1.05rem; opacity:0.95;">{details['overview']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Trailer
                if details['trailer_url']:
                    st.markdown("---")
                    st.markdown('<div class="section-title">🎥 Official Trailer</div>', unsafe_allow_html=True)
                    st.video(details['trailer_url'])
                else:
                    st.warning("⚠️ No trailer available for this movie at the moment")

            # Recommendations
            st.markdown("---")
            st.markdown('<div class="section-title">🌟 Your Perfect Matches</div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align:center; font-size:1.2rem; color:#a8b2d1; margin-bottom:2rem;">Based on advanced AI similarity analysis</p>', unsafe_allow_html=True)
            
            cols = st.columns(5)
            for c,(title,score) in zip(cols,recs):
                with c:
                    if show_posters:
                        poster = get_movie_poster(title)
                        st.markdown('<div class="img-container">', unsafe_allow_html=True)
                        st.image(poster, use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    score_html = f'<div class="similarity-badge">🎯 {score:.1%} Match</div>' if show_scores else ''
                    st.markdown(f"""
                    <div class="movie-card">
                        <strong style="font-size:1.15rem; line-height:1.4;">{title}</strong>
                        {score_html}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Fun fact section
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align:center; padding:2rem; background:rgba(255,255,255,0.03); border-radius:20px; margin:2rem 0;">
                <h3 style="color:#48dbfb; font-size:1.5rem; margin-bottom:1rem;">💡 Did You Know?</h3>
                <p style="font-size:1.1rem; color:#a8b2d1; line-height:1.8;">
                    Our AI analyzed <strong style="color:#feca57;">{len(movies):,}</strong> movies to find these <strong style="color:#feca57;">5</strong> perfect matches for you!<br>
                    The recommendation engine uses <strong style="color:#ff6b6b;">cosine similarity</strong> to calculate compatibility scores.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Oops! We couldn't find that movie in our database. Try selecting another one.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p style="font-size:1.4rem; font-weight:700; background:linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
            🚀 CINEMATCH - Powered by AI & Machine Learning
        </p>
        <p style="font-size:1.05rem; margin-top:1.5rem;">
            ✨ <strong>Features:</strong> Mood-Based Discovery • Age-Appropriate Filtering • Advanced Cosine Similarity Algorithm • Real-Time TMDB Integration
        </p>
        <p style="margin-top:1.5rem; font-size:0.95rem; opacity:0.7;">
            Built with 💜 using Python • Streamlit • Scikit-learn • TMDB API
        </p>
        <p style="margin-top:1rem; color:#667eea; font-weight:600;">
            © 2024 CineMatch | Your Personal Movie Companion
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__=="__main__":
    main()