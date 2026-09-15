import streamlit as st
import pickle
import faiss
import requests
import os

from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="AI Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)


# ==========================
# Load API Key
# ==========================

load_dotenv()

TMDB_KEY = os.getenv(
    "TMDB_API_KEY"
)



# ==========================
# Load Resources
# ==========================

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


    # NEW compressed similarity file
    with open(
        "models/movie_similarity_top50.pkl",
        "rb"
    ) as f:
        movie_similarity = pickle.load(f)


    return model, index, movies, movie_similarity



model, index, movies, movie_similarity = load_resources()



# ==========================
# Clean MovieLens Title
# ==========================

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




# ==========================
# TMDB Details
# ==========================

@st.cache_data
def get_movie_details(title):

    title = clean_title(title)


    url = (
        "https://api.themoviedb.org/3/search/movie"
    )


    params = {

        "api_key": TMDB_KEY,

        "query": title

    }


    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    placeholder = (
        "https://via.placeholder.com/"
        "150x220?text=No+Poster"
    )


    if data.get("results"):

        movie = data["results"][0]


        poster = placeholder


        if movie.get("poster_path"):

            poster = (
                "https://image.tmdb.org/t/p/w500/"
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


        return poster, rating, overview



    return (
        placeholder,
        "N/A",
        "No description available"
    )





# ==========================
# Hybrid Recommendation
# ==========================

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


    recommendation_data = []



    for movie_index, distance in zip(
        indices[0],
        distances[0]
    ):


        semantic_score = 1 / (
            1 + distance
        )


        # New compressed similarity handling
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

            (1 - ai_weight) * rating_score

        )



        recommendation_data.append(

            {
                "movie_index": movie_index,
                "semantic_score": semantic_score,
                "rating_score": rating_score,
                "match_score": final_score
            }

        )



    recommendation_data = sorted(
        recommendation_data,
        key=lambda x: x["match_score"],
        reverse=True
    )



    selected = recommendation_data[:n]



    movie_indices = [

        x["movie_index"]

        for x in selected

    ]



    result = movies.iloc[
        movie_indices
    ].copy()



    result["semantic_score"] = [

        x["semantic_score"]

        for x in selected

    ]


    result["rating_score"] = [

        x["rating_score"]

        for x in selected

    ]


    result["match_score"] = [

        x["match_score"]

        for x in selected

    ]



    return result





# ==========================
# Explanation
# ==========================

def generate_explanation(movie):

    reasons = []


    if movie["semantic_score"] > 0.4:

        reasons.append(
            "Strong match with your description"
        )


    if movie["rating_score"] > 0.05:

        reasons.append(
            "Similar users rated this movie positively"
        )


    if len(reasons) == 0:

        reasons.append(
            "Recommended based on AI similarity"
        )


    return reasons




# ==========================
# Sidebar
# ==========================

st.sidebar.title(
    "⚙️ Recommendation Settings"
)



num_recommendations = st.sidebar.slider(
    "Number of Recommendations",
    5,
    20,
    10
)



ai_weight = st.sidebar.slider(
    "AI Similarity Weight",
    0.0,
    1.0,
    0.6,
    0.1
)



minimum_rating = st.sidebar.slider(
    "Minimum TMDB Rating",
    0.0,
    10.0,
    0.0,
    0.5
)




# ==========================
# Main UI
# ==========================

st.title(
    "🎬 AI Movie Recommendation System"
)


st.write(
    "Describe the movie you want and AI will recommend similar movies."
)



query = st.text_input(
    "🔍 Movie Preference",
    placeholder="Example: space adventure with astronauts"
)



if st.button("Recommend"):


    if query.strip() == "":

        st.warning(
            "Please enter a movie preference."
        )


    else:


        results = hybrid_recommend(
            query,
            n=num_recommendations,
            ai_weight=ai_weight
        )


        st.subheader(
            "Recommended Movies"
        )


        max_score = results[
            "match_score"
        ].max()



        for _, movie in results.iterrows():


            poster, rating, overview = get_movie_details(
                movie["title"]
            )


            if rating != "N/A":

                if float(rating) < minimum_rating:

                    continue



            match_percentage = round(

                (
                    movie["match_score"]
                    /
                    max_score
                )
                *
                100,

                2

            )



            col1, col2 = st.columns(
                [1, 4]
            )



            with col1:

                st.image(
                    poster,
                    width=180
                )



            with col2:


                st.markdown(
                    f"## 🎬 {movie['title']}"
                )


                st.write(
                    "🎭 Genre:",
                    movie["genres"]
                )



                if rating != "N/A":

                    rating = round(
                        float(rating),
                        1
                    )



                st.write(
                    "⭐ Rating:",
                    rating
                )


                st.write(
                    "🤖 AI Match:",
                    str(match_percentage)
                    +
                    "%"
                )



                st.write(
                    "💡 Why recommended?"
                )



                for reason in generate_explanation(movie):

                    st.write(
                        "✓",
                        reason
                    )



                st.write(
                    overview
                )



            st.divider()