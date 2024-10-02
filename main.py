import pandas as pd
import numpy as np
from fastapi import FastAPI
from clickhouse_driver import Client


app = FastAPI()

client = Client('127.0.0.1', port=9000)
db = client.execute('use book_recommendation')

@app.get(
    path="/health",
    tags=["Health"],
)
async def health() -> list:
    result = client.execute('select * from books')
    return result

@app.get(
    path="/love",
    tags=["Love"],
)
async def love() -> str:
    love_string = 'Ты мой самый любимый малышик <3'
    return love_string
