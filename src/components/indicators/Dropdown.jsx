import React from "react";
import styles from "./Dropdown.module.css";

const Dropdown = ({ options, onSelect }) => {
    return (
        <div className={styles.dropdownContainer}>
            <label className={styles.label}>Select an option:</label>
            <select onChange={(e) => onSelect( e.target.value)} className={styles.dropdown}>
                {options.map((option) => (
                    <option key={option.tickerId} value={option.tickerId}>
                        {option.tickerName}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default Dropdown;
