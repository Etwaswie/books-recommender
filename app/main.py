import pandas as pd
import numpy as np
import typing
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from clickhouse_driver import Client
from recommender import recommend
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Укажите адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client('127.0.0.1', port=9000)
db = client.execute('use book_recommendation')

class BookRecommendation(BaseModel):
    title: str
    section: str
    description: str
    similarity: float

class RecoResponse(BaseModel):
    book_id: int
    recommendations: List[BookRecommendation]

@app.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    result = 'Я жив'
    return result

@app.get(
    path="/love",
    tags=["Love"],
)
async def love() -> str:
    love_string = 'Ты мой самый любимый малышик <3'
    return love_string

@app.get("/search/")
async def search_books(title: str):
    query = f"""
        SELECT id, title
        FROM books_temp
        WHERE title ILIKE '%{title}%' limit 10
    """
    results = client.execute(query)
    return [{"id": row[0], "title": row[1]} for row in results]

@app.get(path="/reco/{book_id}", tags=["Recommendations"], response_model=RecoResponse)
async def get_reco(book_id: int) -> RecoResponse:
    recommendations = recommend(book_id, k=5)  # Возвращает список кортежей

    # Преобразование кортежей в объекты BookRecommendation
    items = [
        BookRecommendation(
            title=reco[0],
            section=reco[1],
            description=reco[2],
            similarity=reco[3]
        )
        for reco in recommendations
    ]

    resp = RecoResponse(book_id=book_id, recommendations=items)
    return resp
