import streamlit as st
import pickle
import faiss
import requests
import os

from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="CineMaya AI",
    layout="wide"
)


# =========================
# Load Environment
# =========================

load_dotenv()

TMDB_KEY = os.getenv(
    "TMDB_API_KEY"
)

GEMINI_KEY = os.getenv(
    "GEMINI_API_KEY"
)


genai.configure(
    api_key=GEMINI_KEY
)


gemini_model = genai.GenerativeModel(
    "gemini-3.6-flash"
)

# =========================
# Load Models
# =========================

@st.cache_resource
def load_resources():

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


    index = faiss.read_index(
        "models/movie_embeddings.index"
    )


    with open(
        "models/movies.pkl",
        "rb"
    ) as f:
        movies = pickle.load(f)


    with open(
        "models/movie_similarity_top50.pkl",
        "rb"
    ) as f:
        movie_similarity = pickle.load(f)


    return (
        model,
        index,
        movies,
        movie_similarity
    )



model, index, movies, movie_similarity = load_resources()



# =========================
# Title Formatting
# =========================

def clean_title(title):

    title = title.rsplit(
        "(",
        1
    )[0].strip()


    if ", The" in title:

        title = "The " + title.replace(
            ", The",
            ""
        )


    elif ", A" in title:

        title = "A " + title.replace(
            ", A",
            ""
        )


    elif ", An" in title:

        title = "An " + title.replace(
            ", An",
            ""
        )


    return title



def format_display_title(title):

    year = ""

    if "(" in title and ")" in title:

        year = title[
            title.find("("):
            title.find(")") + 1
        ]


    return clean_title(title) + " " + year

def format_genres(genres):

    if "|" in genres:
        return genres.replace("|", ", ")

    return ", ".join(genres.split())

def enhance_query(query):

    try:

        prompt = f"""
You are a movie recommendation assistant.

Analyze the user movie preference.

Extract:

Genre:
Mood:
Themes:
Keywords:

Then create a concise semantic search query.

User preference:

{query}
"""


        response = gemini_model.generate_content(
            prompt
        )


        return response.text


    except Exception as e:

        st.warning(
            "AI enhancement unavailable. Using direct search."
        )

        return query

# =========================
# TMDB API
# =========================

@st.cache_data
def get_movie_details(title):

    search_title = clean_title(title)


    url = (
        "https://api.themoviedb.org/3/search/movie"
    )


    params = {

        "api_key": TMDB_KEY,

        "query": search_title

    }


    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    placeholder = (
        "https://via.placeholder.com/"
        "300x450?text=No+Poster"
    )


    if data.get("results"):


        movie = data["results"][0]


        poster = placeholder


        if movie.get("poster_path"):


            poster = (
                "https://image.tmdb.org/t/p/w500"
                +
                movie["poster_path"]
            )



        rating = movie.get(
            "vote_average",
            "N/A"
        )


        overview = movie.get(
            "overview",
            "No description available"
        )


        return (
            poster,
            rating,
            overview
        )



    return (
        placeholder,
        "N/A",
        "No description available"
    )



# =========================
# Hybrid Recommendation
# =========================

def hybrid_recommend(
    query,
    n=10,
    ai_weight=0.6
):


    query_vector = model.encode(
        [query]
    )


    distances, indices = index.search(
        query_vector,
        50
    )


    results = []


    for movie_index, distance in zip(
        indices[0],
        distances[0]
    ):


        semantic_score = 1 / (
            1 + distance
        )


        similar_movies = movie_similarity.get(
            movie_index,
            []
        )


        if len(similar_movies) > 0:


            rating_score = sum(
                score
                for _, score in similar_movies
            ) / len(similar_movies)


        else:

            rating_score = 0



        final_score = (

            ai_weight * semantic_score

            +

            (1-ai_weight) * rating_score

        )


        results.append(

            {

                "index": movie_index,

                "semantic": semantic_score,

                "rating": rating_score,

                "score": final_score

            }

        )



    results = sorted(

        results,

        key=lambda x:x["score"],

        reverse=True

    )


    selected = results[:n]


    movie_indices = [

        x["index"]

        for x in selected

    ]


    output = movies.iloc[

        movie_indices

    ].copy()



    output["match_score"] = [

        x["score"]

        for x in selected

    ]



    output["semantic_score"] = [

        x["semantic"]

        for x in selected

    ]



    output["rating_score"] = [

        x["rating"]

        for x in selected

    ]



    return output



# =========================
# Explanation
# =========================

def explanation(movie):

    reasons = []


    semantic_score = movie["semantic_score"]
    rating_score = movie["rating_score"]


    # Semantic AI match
    if semantic_score >= 0.5:

        reasons.append(
            "Strong match with your movie description"
        )

    elif semantic_score >= 0.3:

        reasons.append(
            "Matches the themes and concepts you requested"
        )


    # User preference similarity
    if rating_score >= 0.15:

        reasons.append(
            "Similar viewers showed strong interest in related movies"
        )

    elif rating_score >= 0.05:

        reasons.append(
            "Related movies received positive user ratings"
        )


    # Overall recommendation reason
    if semantic_score > 0.4 and rating_score > 0.1:

        reasons.append(
            "Recommended through a combination of AI understanding and user preference patterns"
        )


    if not reasons:

        reasons.append(
            "Recommended through semantic AI similarity"
        )


    return reasons


# =========================
# Sidebar
# =========================

st.sidebar.title(
    "Settings"
)


number_movies = st.sidebar.slider(

    "Number of recommendations",

    5,

    20,

    10

)



ai_weight = st.sidebar.slider(

    "Semantic AI Weight",

    0.0,

    1.0,

    0.6,

    0.1

)

# =========================
# Main Interface
# =========================

st.title(
    "CineMaya AI"
)


st.caption(
    "Discover movies with Cinemaya"
)



st.write(
    "Describe your movie preference and CineMaya AI will find similar movies."
)



st.markdown(

    """
    <div style="
    background-color:#1f2937;
    padding:18px;
    border-radius:12px;
    ">

    <h4 style="color:#60a5fa;">
    Example query
    </h4>

    <p>
    Romantic comedy from the 2000s
    </p>

    </div>

    """,

    unsafe_allow_html=True

)



# =========================
# Search
# =========================

with st.form(
    "search_form"
):


    query = st.text_input(
        "Your movie preference"
    )


    submit = st.form_submit_button(
        "Recommend Movies"
    )




if submit:

    if query.strip() == "":

        st.warning(
            "Please enter a movie preference."
        )

    else:

        enhanced_query = enhance_query(
            query
        )


        with st.expander(
            "CineMaya AI Analysis"
        ):

            st.write(
                enhanced_query
            )


        with st.spinner(
            "CineMaya AI is finding the best movies..."
        ):

            results = hybrid_recommend(

                enhanced_query,

                n=number_movies,

                ai_weight=ai_weight

            )


        st.subheader(
            "Recommended Movies"
        )


        max_score = float(

            results["match_score"].max()

        )



        for _, movie in results.iterrows():



            poster, rating, overview = get_movie_details(

                movie["title"]

            )



            match = round(

                float(

                    (

                        movie["match_score"]

                        /

                        max_score

                    )

                    * 100

                ),

                1

            )



            col1, col2 = st.columns(

                [1,4]

            )



            with col1:


                st.image(

                    poster,

                    width=170

                )



            with col2:


                st.markdown(

                    f"## {format_display_title(movie['title'])}"

                )


                st.write(

                    "Genre:",

                    format_genres(movie["genres"])

                )



                if rating != "N/A":


                    rating = round(

                        float(rating),

                        1

                    )



                st.write(

                    "Rating:",

                    rating

                )



                st.progress(

                    float(match/100)

                )



                st.write(

                    f"AI Relevance Score: {match}%"

                )

                semantic_percentage = round(
                   float(movie["semantic_score"]) * 100,
                   1
                )


                rating_percentage = round(
                   float(movie["rating_score"]) * 100,
                   1
                )


                with st.expander("Score Breakdown"):

                  st.write(
                      f"Semantic Understanding: {semantic_percentage}%"

                  )

                  st.write(
                      f"User Preference Signal: {rating_percentage}%"

                  )

                st.write(

                    "Why recommended:"

                )



                for item in explanation(movie):


                    st.write(

                        "•",

                        item

                    )



                st.write(

                    overview

                )



            st.divider()

    st.caption(
        "CineMaya AI | Built with Gemini, Sentence Transformers, FAISS and Streamlit"
    )      