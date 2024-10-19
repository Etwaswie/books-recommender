// src/BookSearch.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './BookSearch.css'; // Импортируйте CSS файл

const BookSearch = ({ onSelect, onGetRecommendations }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);

    useEffect(() => {
        const fetchBooks = async () => {
            if (searchTerm.length > 2) {
                try {
                    const response = await axios.get(`http://127.0.0.1:8000/search/?title=${searchTerm}`);
                    setResults(response.data); // Предполагается, что response.data содержит массив книг
                } catch (error) {
                    console.error('Ошибка при поиске книг:', error);
                }
            } else {
                setResults([]);
            }
        };

        const timeoutId = setTimeout(fetchBooks, 300);
        return () => clearTimeout(timeoutId);
    }, [searchTerm]);

    const handleSelect = (book) => {
        setSearchTerm(book.title);
        setResults([]);
        onSelect(book);
    };

    const handleGetRecommendations = () => {
        onGetRecommendations(searchTerm);
    };

    return (
        <div className="book-search">
            <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Введите название книги"
                className="search-input"
            />
            {results.length > 0 && (
                <div className="dropdown">
                    {results.map((book) => (
                        <div
                            key={book.id}
                            className="dropdown-item"
                            onClick={() => handleSelect(book)}
                        >
                            {book.title}
                        </div>
                    ))}
                </div>
            )}
            <button onClick={handleGetRecommendations} disabled={!searchTerm}>
                Получить рекомендации
            </button>
        </div>
    );
};

export default BookSearch;
