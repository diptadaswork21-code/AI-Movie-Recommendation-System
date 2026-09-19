# 🎬 CineMaya AI Architecture

## Overview

CineMaya AI is an AI-powered hybrid movie recommendation system that combines Generative AI, semantic search, and collaborative filtering to recommend movies based on natural language preferences.

The system understands user intent using Gemini AI, finds semantically similar movies using Sentence Transformers and FAISS, then improves ranking using MovieLens rating similarity.

---

# Overall Pipeline


```
                    User Input

Example:
"A space movie with emotional story"

                        |

                        ↓


          Gemini AI Query Understanding Layer

              - Genre extraction
              - Mood detection
              - Theme identification
              - Keyword generation

                        |

                        ↓


              Enhanced Semantic Query

                        |

                        ↓


          Sentence Transformer Model

              (all-MiniLM-L6-v2)

                        |

                        ↓


              Text Embedding Vector

                        |

                        ↓


                  FAISS Index

          Semantic Similarity Search

                        |

                        ↓


             Top Candidate Movies

                        |

                        ↓


        MovieLens Collaborative Filtering

          (Movie Rating Similarity)

                        |

                        ↓


              Hybrid Ranking Model


      Semantic Similarity + Rating Similarity


                        |

                        ↓


                  TMDB API


       Poster | Rating | Description


                        |

                        ↓


              Streamlit Web Application

```

---

# Model Components


## 1. Gemini AI Query Understanding Layer

Purpose:

Convert natural language movie preferences into meaningful search information.

Example:

Input:

```
A space movie with emotional story
```

Gemini extracts:

```
Genre:
Science Fiction, Drama

Mood:
Emotional, Thought-provoking

Themes:
Space exploration, human connection

Keywords:
Astronaut, deep space, survival
```

The generated semantic query improves the quality of vector search by providing richer contextual information.

---

# 2. Sentence Transformer

Model:

```
all-MiniLM-L6-v2
```

Purpose:

Convert the enhanced movie description into numerical embeddings.

The embedding captures the semantic meaning of the user's preference and allows comparison between user queries and movie descriptions.

---

# 3. FAISS Vector Search

Purpose:

Perform fast similarity search between:

- User query embedding
- Movie embedding database


FAISS retrieves the most relevant candidate movies based on semantic similarity.

---

# 4. Collaborative Filtering

Purpose:

Use MovieLens user rating behaviour to identify relationships between movies.

Movies with similar user rating patterns receive higher similarity scores.

This provides a user preference signal in addition to content understanding.

---

# 5. Hybrid Recommendation Engine

The final recommendation score combines two signals:

```
Final Score =

Semantic Similarity × AI Weight

+

Rating Similarity × (1 - AI Weight)

```

## Semantic Similarity

Represents:

- User intent matching
- Movie concept similarity
- Theme relevance


## Rating Similarity

Represents:

- Historical user preference patterns
- Similar movie interactions


The hybrid approach balances AI understanding with collaborative filtering.

---

# 6. TMDB Integration

TMDB API provides additional movie information:

- Movie posters
- Ratings
- Descriptions


---

# 7. Explainable Recommendation System

CineMaya AI provides reasoning behind recommendations.

Examples:

- Strong match with your movie description
- Similar viewers showed interest in related movies
- Recommended through AI similarity and user preference patterns


The system also displays:

- AI relevance score
- Semantic similarity score
- User preference signal

---

# 8. Streamlit Application

The frontend provides:

- Natural language movie search
- Gemini AI understanding display
- Movie recommendations
- Explainable recommendation reasons
- Interactive controls for recommendation settings


---

# Technology Stack


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

# Deployment Flow


```
GitHub Repository

        |

        ↓

Streamlit Cloud

        |

        ↓

Live CineMaya AI Application

```

---

# Future Improvements

Possible future upgrades:

- User authentication
- Personal recommendation history
- More advanced ranking models
- Conversation-based movie assistant
- Multi-language movie search
