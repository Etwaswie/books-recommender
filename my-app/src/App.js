// src/App.js
import React, { useState } from 'react';
import BookSearch from './BookSearch';
import { getRecommendations } from './api'; // Убедитесь, что эта функция правильно экспортируется

const App = () => {
    const [selectedBook, setSelectedBook] = useState(null);
    const [recommendations, setRecommendations] = useState([]);

    const handleBookSelect = (book) => {
        setSelectedBook(book);
    };

    const handleGetRecommendations = async () => {
      if (!selectedBook) return; // Проверяем, выбрана ли книга
      const data = await getRecommendations(selectedBook.id); // Здесь используем ID
      console.log('Полученные рекомендации:', data); // Логируем полученные данные
      setRecommendations(data.recommendations || []); // Устанавливаем рекомендации
  };

    return (
        <div>
            <h1>Система рекомендаций книг</h1>
            <BookSearch onSelect={handleBookSelect} onGetRecommendations={handleGetRecommendations} />
            {selectedBook && (
                <div>
                    <h2>Рекомендации для: {selectedBook.title}</h2>
                    {recommendations.length > 0 ? (
                        <ul>
                            {recommendations.map((item, index) => (
                                <li key={index}>
                                    <h4>{item.title}</h4>
                                    <p>{item.description}</p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>Рекомендации отсутствуют.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default App;
