import React from 'react';
import { Navigate } from 'react-router-dom';
import {jwtDecode} from 'jwt-decode';

const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('token');

    if (!token) {
        return <Navigate to="/login" />;
    }

    try {
        const decodedToken = jwtDecode(token);
        if (decodedToken.role !== 'ADMIN') {
            return <Navigate to="/login" />;
        }
    } catch (error) {
        return <Navigate to="/login" />;
    }

    // If the user is authenticated and authorized, render the children
    return children;
};

export default PrivateRoute;
