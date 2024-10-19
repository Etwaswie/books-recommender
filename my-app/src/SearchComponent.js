import React, { useEffect, useRef, useState } from 'react';

const SearchComponent = ({ onSelect }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const dropdownRef = useRef(null);

    const handleSearch = async (e) => {
        const value = e.target.value;
        setSearchTerm(value);

        if (value.length > 0) {
            const response = await fetch(`/search/?title=${value}`);
            const data = await response.json();
            setResults(data); // Убедитесь, что сервер возвращает массив книг
            setShowDropdown(true);
        } else {
            setResults([]);
            setShowDropdown(false);
        }
    };

    const handleItemClick = (item) => {
        setSearchTerm(item.title);
        setShowDropdown(false);
        onSelect(item); // Вызываем функцию для передачи выбранной книги
    };

    const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
            setShowDropdown(false);
        }
    };

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    return (
        <div>
            <input
                type="text"
                value={searchTerm}
                onChange={handleSearch}
                placeholder="Введите название книги"
            />
            {showDropdown && results.length > 0 && (
                <ul ref={dropdownRef} style={{ border: '1px solid #ccc', maxHeight: '200px', overflowY: 'auto' }}>
                    {results.map((item) => (
                        <li key={item.id} onClick={() => handleItemClick(item)} style={{ cursor: 'pointer' }}>
                            {item.title}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default SearchComponent;
