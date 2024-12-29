import axios from 'axios';
import config from "../config/config";

const BASE_URL = config.API_BASE_URL;

export const register = async (userDTO) => {
    await axios.post(`${BASE_URL}/register`, userDTO);
};

export const login = async (userLoginDTO) => {
    try {
        const response = await axios.post(`${BASE_URL}/login`, userLoginDTO);
        const {token} = response.data;  // Adjust this based on your backend response
        localStorage.setItem('token', token);
        return response;
    }catch (error) {
        console.error('Login failed:', error);
        throw error;


    }
};

export const logout = async () => {
    await axios.post(`${BASE_URL}/logout`);
};
