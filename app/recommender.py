import random
import torch
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import ast

books = pd.read_csv(r"D:\pythonProject\BookRecsys\data\books_embed.csv", engine='python')

def convert_to_float_list(s):
    return [float(num) for num in s.split(', ')]


def recommend(book_id, k=5):
    data_popular = books
    data_popular['embeddings'] = data_popular['str_embeddings'].apply(convert_to_float_list)

    target_embedding = data_popular[data_popular['id'] == book_id]['embeddings'].iloc[0]
    data_choosen = data_popular[data_popular['section'] == data_popular.loc[data_popular['id'] == book_id, 'section'].iloc[0]]
    data_choosen.reset_index(inplace=True, drop=True)

    # Нахождение схожести с остальными текстами
    similarities_subsection = []
    similarities_all = []
    for i in range(len(data_choosen)):
        current_id = data_choosen['id'].iloc[i]
        if current_id != book_id:  # исключаем сам текст
            current_embedding = torch.tensor(data_choosen['embeddings'].iloc[i])
            similarity = util.pytorch_cos_sim(target_embedding, current_embedding).item()
            similarities_subsection.append((data_choosen['title'].iloc[i], data_choosen['section'].iloc[i], data_choosen['description'].iloc[i], similarity))

    for i in range(len(data_popular)):
        current_id = data_popular['id'].iloc[i]
        if current_id != book_id:  # исключаем сам текст
            current_embedding = torch.tensor(data_popular['embeddings'].iloc[i])
            similarity = util.pytorch_cos_sim(target_embedding, current_embedding).item()
            similarities_all.append((data_popular['title'].iloc[i], data_popular['section'].iloc[i], data_popular['description'].iloc[i], similarity))

    # Сортировка по схожести
    similarities_subsection.sort(key=lambda x: x[3], reverse=True)
    similarities_all.sort(key=lambda x: x[3], reverse=True)

    # Вывод 5 самых близких текстов
    # print("Самые близкие тексты с таким же жанром к:", data_choosen[data_choosen['id'] == book_id]['title'].iloc[0], data_choosen[data_choosen['id'] == book_id]['description'].iloc[0])
    # for name, subsection, text, score in similarities_subsection[:k]:
    #     print(f"\n")
    #     print(f"{name}\n{subsection}\n{text}\n(схожесть: {score})")
    # print(f"---------------------------------------------------------\n")
    # print("Самые близкие тексты из всех книг к:", data_popular[data_popular['id'] == book_id]['title'].iloc[0], data_popular[data_popular['id'] == book_id]['description'].iloc[0])
    # for name, subsection, text, score in similarities_all[:k]:
    #     print(f"\n")
    #     print(f"{name}\n{subsection}\n{text}\n(схожесть: {score})")

    reco = similarities_subsection[:k]
    return reco