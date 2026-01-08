import React, { createContext, useState, useEffect } from 'react';
import { authService } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // 1. Check if user is already logged in on page load
    useEffect(() => {
        const storedUser = localStorage.getItem('jamii_user');
        const token = localStorage.getItem('jamii_token');

        if (storedUser && token) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    // 2. Login Function
    const login = async (credentials) => {
        const data = await authService.login(credentials);

        // Save to browser storage
        localStorage.setItem('jamii_token', data.token);
        localStorage.setItem('jamii_user', JSON.stringify({
            username: data.username,
            ward: data.ward
        }));

        setUser({ username: data.username, ward: data.ward });
        return data;
    };

    // 3. Logout Function
    const logout = () => {
        localStorage.removeItem('jamii_token');
        localStorage.removeItem('jamii_user');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
