# 🎬 AI Movie Recommendation System Architecture


## Overall Pipeline


```
                    User Input

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


       Semantic Score + Rating Score


                        |

                        ↓


                  TMDB API


       Poster | Rating | Description


                        |

                        ↓


              Streamlit Web App

```

---

# Model Components


## 1. Sentence Transformer

Purpose:

Convert natural language movie preferences into numerical embeddings.

Example:

Input:

```
space adventure with astronauts
```

Output:

Embedding vector representing the meaning of the query.


---

## 2. FAISS Vector Search

Purpose:

Perform fast similarity search between user query embeddings and movie embeddings.

The system retrieves the most relevant movies from the embedding database.


---

## 3. Collaborative Filtering

Purpose:

Use MovieLens rating behavior to understand relationships between movies.

Movies with similar user rating patterns receive higher similarity scores.


---

## 4. Hybrid Ranking

The final recommendation score combines:

```
Final Score =

Semantic Similarity × 0.6

+

Rating Similarity × 0.4
```

This balances user intent and historical preference patterns.


---

## 5. TMDB Integration

TMDB API provides:

- Movie posters
- Ratings
- Movie descriptions


---

## Deployment Flow


```
GitHub Repository

        |

        ↓

Streamlit Cloud

        |

        ↓

Live AI Recommendation Application

```