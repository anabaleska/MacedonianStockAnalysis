import React from 'react';
import styles from './Input.module.css';

export const Input = ({ label, type = "text", placeholder, value, onChange }) => {
    const inputId = `${label.toLowerCase()}-input`;

    return (
        <div className={styles.inputContainer}>
            <label htmlFor={inputId} className={styles.inputLabel}>{label}</label>
            <input
                id={inputId}
                type={type}
                className={styles.inputField}
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}  // Handling the input change
                aria-label={label}
            />
        </div>
    );
};
