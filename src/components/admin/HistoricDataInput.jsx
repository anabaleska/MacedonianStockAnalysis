import * as React from "react";
import styles from './HistoricDataInput.module.css';

export default function HistoricDataInput() {
    return (
        <form className={styles.container}>
            <h1 className={styles.title}>Historic Data</h1>
            <div className={styles.inputContainer}>
                <div>
                    <label htmlFor="tickerInput" className={styles['visually-hidden']}>Ticker name</label>
                    <input
                        id="tickerInput"
                        type="text"
                        className={styles.input}
                        placeholder="Ticker name"
                        aria-label="Ticker name"
                    />
                </div>
                <div className={styles.dateContainer}>
                    <div>
                        <label htmlFor="dateInput" className={styles['visually-hidden']}>Date</label>
                        <input
                            id="dateInput"
                            type="date"
                            className={styles.input}
                            aria-label="Date"
                        />
                    </div>
                    <img
                        loading="lazy"
                        src="https://cdn.builder.io/api/v1/image/assets/TEMP/19e390e73f7343a0e58e75d3471c3aa422d7e1038c640b6df9b408972085d86b?placeholderIfAbsent=true&apiKey=60217a24597e419ca472b84d3fa7f5bd"
                        className={styles.calendarIcon}
                        alt=""
                        role="presentation"
                    />
                </div>
            </div>
        </form>
    );
}