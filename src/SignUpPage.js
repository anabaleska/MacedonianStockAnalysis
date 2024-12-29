import React, { useState } from 'react';
import { Input } from './components/login/Input';
import styles from './LoginPage.module.css';
import { useNavigate } from 'react-router-dom';
import { register } from './service/UserService'; // Import the register function

export const SignUpPage = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [repeatedPassword, setRepeatedPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');  // For error messages

    const navigate = useNavigate();

    const handleLoginClick = () => {
        navigate('/login');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate passwords match
        if (password !== repeatedPassword) {
            setErrorMessage("Passwords do not match.");
            return;
        }

        const userDTO = {
            email,
            username,
            password,
            repeatedPassword,
        };

        try {
            // Call the register function from your service
            await register(userDTO);

            // Redirect to the login page after successful registration
            navigate('/login');
        } catch (error) {
            setErrorMessage('Sign up failed. Please try again later.');
            console.error('Sign up failed:', error);
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

                <h2 className={styles.loginTitle}>Sign up to continue</h2>

                {errorMessage && <p className={styles.error}>{errorMessage}</p>} {/* Display error message if any */}

                <form onSubmit={handleSubmit} className={styles.form}>
                    <Input
                        label="Email"
                        type="email"
                        placeholder="example@gmail.com"
                        value={email}
                        onChange={setEmail}
                    />
                    <Input
                        label="Username"
                        type="text"
                        placeholder="username"
                        value={username}
                        onChange={setUsername}
                    />
                    <Input
                        label="Password"
                        type="password"
                        placeholder="password"
                        value={password}
                        onChange={setPassword}
                    />
                    <Input
                        label="Repeat Password"
                        type="password"
                        placeholder="password"
                        value={repeatedPassword}
                        onChange={setRepeatedPassword}
                    />

                    <button
                        type="submit"
                        className={styles.loginButton}
                    >
                        Sign Up
                    </button>

                    <button
                        type="button"
                        className={styles.signupLink}
                        tabIndex={0}
                        onClick={handleLoginClick}
                    >
                        Already have an account? <span className={styles.signupText}>Login</span>
                    </button>
                </form>
            </div>
        </div>
    );
};
