# 🎬 CineMaya AI
## AI-Powered Hybrid Movie Recommendation System


CineMaya AI is an intelligent movie recommendation system that understands natural language preferences and recommends movies using Generative AI, semantic search, and collaborative filtering.

Instead of searching only by movie titles or genres, users can describe the type of movie they want:

Example:

> "A space movie with emotional story"

The system analyzes the request using Gemini AI, creates a richer semantic representation, and finds relevant movies through AI-powered similarity search.


---

# 🚀 Live Demo

Streamlit Application:

(Add your Streamlit URL here)


---

# ✨ Features


## 🤖 Gemini AI Query Understanding

CineMaya AI uses Google Gemini to analyze user preferences and extract:

- Genre
- Mood
- Themes
- Keywords

Example:

Input:

```
A space movie with emotional story
```

AI Understanding:

```
Genre:
Science Fiction, Drama

Mood:
Emotional, Thought-provoking

Themes:
Space exploration, human connection
```


---

## 🔎 Semantic Movie Search

The system uses Sentence Transformer embeddings to understand the meaning behind user queries.

Model:

```
all-MiniLM-L6-v2
```

This allows users to search naturally without knowing exact movie titles.


---

## ⚡ FAISS Similarity Search

FAISS is used for efficient vector similarity search.

The system compares:

- User query embeddings
- Movie embeddings

and retrieves the most relevant candidates.


---

## 🎯 Hybrid Recommendation Engine

CineMaya combines two recommendation signals:

```
Final Score =

Semantic Similarity × AI Weight

+

Rating Similarity × (1 - AI Weight)
```


### Semantic Similarity

Measures:

- Query relevance
- Theme similarity
- Context matching


### Rating Similarity

Uses MovieLens rating behaviour to understand relationships between movies.


---

## 🎬 TMDB Integration

TMDB API provides:

- Movie posters
- Ratings
- Movie descriptions


---

## 💡 Explainable Recommendations

CineMaya explains why a movie was recommended.

Examples:

- Strong match with your movie description
- Similar viewers showed interest in related movies
- Recommended through AI similarity and preference signals


---

# 🏗️ System Architecture


```
User Query

     ↓

Gemini AI Query Understanding

     ↓

Enhanced Semantic Query

     ↓

Sentence Transformer Embedding

     ↓

FAISS Vector Search

     ↓

Hybrid Ranking Model

     ↓

TMDB Information Retrieval

     ↓

Streamlit Application

```


Detailed architecture:

See:

```
docs/architecture.md
```


---

# 🛠️ Technology Stack


## Generative AI

- Google Gemini API


## Machine Learning

- Sentence Transformers
- FAISS
- Collaborative Filtering


## Backend

- Python


## Frontend

- Streamlit


## External API

- TMDB API


---

# 📂 Project Structure


```
AI-Movie-Recommendation-System

│
├── app
│   └── app.py
│
├── data
│   ├── movies.csv
│   └── ratings.csv
│
├── models
│   ├── movie_embeddings.index
│   ├── movie_embeddings.pkl
│   ├── movie_similarity_top50.pkl
│   └── movies.pkl
│
├── notebooks
│   └── 01_movie_recommendation_basics.ipynb
│
├── docs
│   └── architecture.md
│
├── screenshots
│
├── requirements.txt
│
└── README.md

```


---

# ⚙️ Installation


Clone repository:

```bash
git clone https://github.com/diptadaswork21-code/CineMaya-AI.git 
```


Create virtual environment:

```bash
python -m venv .venv
```


Activate environment:

Windows:

```bash
.venv\Scripts\activate
```


Install dependencies:

```bash
pip install -r requirements.txt
```


Create `.env` file:

```
TMDB_API_KEY=your_tmdb_api_key

GEMINI_API_KEY=your_gemini_api_key
```


Run application:

```bash
streamlit run app/app.py
```


---

# 📸 Screenshots


(Add screenshots here)

Examples:

- Home page
- AI Understanding panel
- Recommendation results


---

# 🔮 Future Improvements


Possible improvements:

- User login and personalized profiles
- Conversation-based movie assistant
- Advanced recommendation models
- User recommendation history
- Multi-language support


---

# 👨‍💻 Author

Sudipta Das

AI / Machine Learning Enthusiast

GitHub:
https://github.com/diptadaswork21-code

