# 🎬 AI Movie Recommendation System

An AI-powered movie recommendation system using semantic search, collaborative filtering, and hybrid recommendation techniques.

---

## 🚀 Features

- AI semantic movie search using Sentence Transformers
- FAISS vector similarity search
- MovieLens collaborative filtering
- Hybrid recommendation model
- TMDB API integration
- Movie posters, ratings, and descriptions
- Explainable AI recommendations
- Interactive Streamlit interface

---

## 🏗️ System Architecture

```
User Query

↓

Sentence Transformer Embedding

↓

FAISS Semantic Search

↓

MovieLens Rating Similarity

↓

Hybrid Ranking

↓

TMDB Movie Information

↓

Streamlit Application
```

---

## 🧠 Recommendation Approach

The system combines three recommendation techniques:

### 1. Content-Based Filtering

The system analyzes movie information such as titles, genres, and descriptions to understand the user's natural language preference.

Sentence Transformer converts text information into numerical embeddings, allowing semantic similarity search.

### 2. Collaborative Filtering

The system uses MovieLens user rating patterns to identify relationships between movies based on user preferences.

Movies liked by similar users influence the final recommendation ranking.

### 3. Hybrid Recommendation

The final recommendation score combines semantic similarity and rating similarity:

```
Final Score =

0.6 × Semantic Similarity

+

0.4 × Rating Similarity
```

Semantic similarity helps understand the user's query, while rating similarity improves personalization using historical user behavior.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Sentence Transformers
- FAISS
- Scikit-learn
- MovieLens Dataset
- TMDB API
- Pandas
- NumPy

---

## 📂 Project Structure

```
movie-recommendation-ai/

│
├── app/
│   └── app.py
│
├── models/
│   ├── movie_embeddings.index
│   ├── movies.pkl
│   └── movie_similarity_rating.pkl
│
├── data/
│
├── notebooks/
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

## ⚙️ How It Works

1. User enters a natural language movie preference.
2. Sentence Transformer converts the query into an embedding vector.
3. FAISS performs semantic similarity search to find relevant movies.
4. MovieLens rating similarity adjusts recommendations based on user behavior.
5. Hybrid ranking generates the final recommendation list.
6. TMDB API provides movie posters, ratings, and descriptions.
7. The Streamlit interface displays the recommended movies.

---

## ▶️ Installation & Usage

### 1. Clone the Repository

```bash
git clone your-repository-url
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add TMDB API Key

Create a `.env` file in the project root:

```
TMDB_API_KEY=your_api_key_here
```

### 4. Run the Application

```bash
streamlit run app/app.py
```

---

## 🎯 Application Features

The application allows users to:

- Search movies using natural language descriptions
- Adjust AI similarity and rating influence
- Select the number of recommendations
- Filter movies based on minimum rating
- View movie posters, ratings, and descriptions
- Understand why a movie was recommended through explainable AI feedback

---

## 🔮 Future Improvements

- User profile-based recommendations
- Personalized recommendation history
- Advanced deep learning recommendation models
- Model evaluation using Precision@K and NDCG
- Cloud deployment
- Continuous learning from user feedback

---

## 👨‍💻 Author

AI Movie Recommendation System developed using Python, Machine Learning, Natural Language Processing, and Recommendation System techniques.