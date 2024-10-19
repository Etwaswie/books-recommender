// src/BookRecommendationForm.js
import React, { useState } from 'react';
import { getRecommendations } from './api';

const BookRecommendationForm = () => {
    const [bookId, setBookId] = useState('');
    const [recommendations, setRecommendations] = useState([]);

    const handleInputChange = (e) => {
        setBookId(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); // предотвращаем перезагрузку страницы
        if (!bookId) return; // если ID книги не введён, ничего не делаем

        try {
            const data = await getRecommendations(bookId);
            setRecommendations(data.recommendations);
        } catch (error) {
            console.error('Ошибка при получении рекомендаций:', error);
        }
    };

    return (
        <div>
            <h2>Получить рекомендации по книге</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="number"
                    value={bookId}
                    onChange={handleInputChange}
                    placeholder="Введите ID книги"
                    required
                />
                <button type="submit">Получить рекомендации</button>
            </form>

            {recommendations.length > 0 && (
                <div>
                    <h3>Рекомендации:</h3>
                    <ul>
                        {recommendations.map((item, index) => (
                            <li key={index}>
                                <h4>{item.title}</h4>
                                <p>{item.description}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default BookRecommendationForm;
