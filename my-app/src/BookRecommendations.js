// src/BookRecommendations.js
import React, { useEffect, useState } from 'react';
import { getRecommendations } from './api';

const BookRecommendations = ({ bookId }) => {
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const data = await getRecommendations(bookId);
                setRecommendations(data.recommendations);
            } catch (error) {
                console.error('Ошибка при получении рекомендаций:', error);
            }
        };

        fetchRecommendations();
    }, [bookId]);

    return (
        <div>
            <h2>Рекомендации для книги ID: {bookId}</h2>
            <ul>
                {recommendations.map((item, index) => (
                    <li key={index}>
                        <h3>{item.title}</h3>
                        <p>{item.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default BookRecommendations;
