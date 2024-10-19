import torch
import re
import nltk
import pymorphy3

from clickhouse_driver import Client
from sentence_transformers import SentenceTransformer, util
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt_tab')
# nltk.download('omw-1.4')

morph = pymorphy3.MorphAnalyzer()
stop_words_russian = stopwords.words('russian')

model = SentenceTransformer('all-MiniLM-L6-v2')

# Подключение к ClickHouse
client = Client('127.0.0.1', port=9000)
db = client.execute('use book_recommendation')

def prepare_text(text):
    if text is None or text.strip() == '':  # Проверка на None или пустую строку
        return []  # Возвращаем пустые значения, чтобы избежать ошибки

    text = text.lower()  # Приведение к нижнему регистру
    text = re.sub(r'\W+', ' ', text)  # Удаление лишних символов
    tokenized = word_tokenize(text)  # Токенизация
    lemm_text = [morph.parse(word)[0].normal_form for word in tokenized if word not in stop_words_russian]

    return ' '.join(lemm_text)

# Шаг 1: Извлечение описаний книг из ClickHouse
query = 'SELECT id, description FROM books_temp'
books_data = client.execute(query)

# Шаг 2: Подготовка обновлений
batch_size = 5
total_books = len(books_data)

for i in range(0, total_books, batch_size):
    # Обработка 100 текстов
    batch_books = books_data[i:i + batch_size]
    updates = []

    for book_id, description in batch_books:
        cleaned_description = prepare_text(description)

        if cleaned_description:  # Проверка на непустую строку
            embedding = model.encode(cleaned_description).tolist()  # Получаем эмбеддинг
            updates.append((book_id, embedding))

    # Обновление 100 строк
    if updates:
        update_cases = ' '.join(
            f'WHEN id = {book_id} THEN array({", ".join(map(str, embedding))})'
            for book_id, embedding in updates
        )

        update_query = f"""
            ALTER TABLE books_temp
            UPDATE embedding = CASE {update_cases}
                ELSE embedding
            END
            WHERE id IN ({', '.join(str(book_id) for book_id, _ in updates)});
        """

        try:
            client.execute(update_query)
            print(f"Batch {i // batch_size + 1} updated successfully.")
        except Exception as e:
            print(f"Error updating batch {i // batch_size + 1}: {e}")

# Шаг 4: Оптимизация таблицы
client.execute('OPTIMIZE TABLE books_temp')

# query = 'SELECT id, cleaned_description FROM books_temp'
# cleaned_books_data = client.execute(query)

# book_ids = []
# descriptions = []
# for book in cleaned_books_data:
#     book_ids.append(book[0])
#     descriptions.append(book[1])

# # Используем модель для вычисления эмбеддингов
# embeddings = model.encode(descriptions)

# # Шаг 4: Запись эмбеддингов обратно в ClickHouse
# for book_id, embedding in zip(book_ids, embeddings):
#     # Преобразуем векторы в формат, подходящий для ClickHouse (например, массив float32)
#     embedding_list = embedding.tolist()  # Преобразуем тензор в список
#     client.execute(
#         f'ALTER TABLE books_temp UPDATE embedding = \'{embedding_list}\' WHERE id = {book_id}'
#     )