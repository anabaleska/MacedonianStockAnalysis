import React, { useState } from 'react';
import { Input } from './components/login/Input';  // Adjust import path for InputField
import styles from './LoginPage.module.css';
import { useNavigate } from 'react-router-dom';
import { login } from './service/UserService';  // Import login function
import { jwtDecode } from 'jwt-decode';



export const LoginPage = () => {
    const [email, setEmail] = useState('');  // State for email
    const [password, setPassword] = useState('');  // State for password
    const [errorMessage, setErrorMessage] = useState('');  // For error messages

    const navigate = useNavigate();

    const handleSignupClick = () => {
        navigate('/sign-up');  // Navigate to the sign-up page
    };

    const handleSubmit = async (e) => {
        e.preventDefault();  // Prevent default form submission behavior

        const userLoginDTO = {  // Object for sending the login data
            email,
            password,
        };

        try {
            // Call the login function from your service
            const response = await login(userLoginDTO);

            const token = localStorage.getItem('token');
            const decodedToken = jwtDecode(token);
            // Redirect to the dashboard after successful login
            if (decodedToken.role === 'ADMIN') {
                navigate('/admin');
            } else {
                navigate('/');
            }
        } catch (error) {
            // Display error message in case of failed login
            setErrorMessage('Login failed. Please check your credentials or try again later.');
            console.error('Login failed:', error);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.content}>
                <h1 className={styles.title}>
                    Macedonian
                    <br />
                    <span className={styles.highlight}>Stock</span> Analysis
                </h1>

                <h2 className={styles.loginTitle}>Login</h2>

                {/* Display error message if there's any */}
                {errorMessage && <p className={styles.error}>{errorMessage}</p>}

                {/* Login Form */}
                <form onSubmit={handleSubmit} className={styles.form}>
                    {/* Controlled Input for Email */}
                    <Input
                        label="Email"
                        value={email}  // Controlled input
                        onChange={setEmail}  // Update email state
                        type="email"
                        required
                        placeholder="example@gmail.com"
                    />

                    {/* Controlled Input for Password */}
                    <Input
                        label="Password"
                        value={password}  // Controlled input
                        onChange={setPassword}  // Update password state
                        type="password"
                        required
                        placeholder="Enter your password"
                    />

                    {/* Submit Button */}
                    <button type="submit" className={styles.loginButton}>
                        Login
                    </button>

                    {/* Sign Up Link */}
                    <button
                        type="button"
                        className={styles.signupLink}
                        onClick={handleSignupClick}
                    >
                        Don't have an account? <span className={styles.signupText}>Sign Up</span>
                    </button>
                </form>
            </div>
        </div>
    );
};
