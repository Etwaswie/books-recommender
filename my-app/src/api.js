// src/api.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const getRecommendations = async (bookId) => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/reco/${bookId}`);
        return response.data; // Убедитесь, что сервер возвращает данные в ожидаемом формате
    } catch (error) {
        console.error('Ошибка при получении рекомендаций:', error);
        return { recommendations: [] }; // Возвращаем пустой массив в случае ошибки
    }
};
