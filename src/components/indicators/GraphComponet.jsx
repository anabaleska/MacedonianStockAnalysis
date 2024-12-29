import React from "react";
import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";
import styles from "./GraphComponent.module.css";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const GraphComponent = ({tickerId}) => {

    const [indicators, setIndicators] = useState([]);

    useEffect(() => {
        if (!tickerId) return;

        const fetchIndicators = async () => {

            try {
                const response = await fetch(`http://localhost:8081/api/stock-indicators/${tickerId}`);
                const data = await response.json();
                setIndicators(data);
            } catch (error) {
                console.error("Error fetching indicators:", error);
            }
        };

        fetchIndicators();
    }, [tickerId]);

    const chartData = {
        labels: indicators.map((item) => (item.date.split("T")[0])), // Assuming date is in a usable format
        datasets: [
            {
                label: "SMA 50",
                data: indicators.map(item => item.sma50),
                borderColor: "blue",
                fill: false,
            },
            {
                label: "SMA 200",
                data: indicators.map(item => item.sma200),
                borderColor: "green",
                fill: false,
            },
            {
                label: "EMA 50",
                data: indicators.map(item => item.ema50),
                borderColor: "orange",
                fill: false,
            },
            {
                label: "EMA 200",
                data: indicators.map(item => item.ema200),
                borderColor: "red",
                fill: false,
            },
            {
                label: "RSI",
                data: indicators.map(item => item.rsi),
                borderColor: "purple",
                fill: false,
            },
        ],
    };

    return (
        <div className={styles.graphContainer}>
            <h2>Technical Indicators for Ticker {tickerId}</h2>
            <Line data={chartData} />
        </div>
    );
};

export default GraphComponent;
