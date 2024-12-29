import React, {useState, useEffect} from 'react';
import Select from 'react-select';
import {Line} from 'react-chartjs-2';
import axios from 'axios';

const Predictions = () => {
    const [tickers, setTickers] = useState([]);
    const [selectedTicker, setSelectedTicker] = useState(null);
    const [chartData, setChartData] = useState(null);
    const [finalPrediction, setFinalPrediction] = useState(null);
    useEffect(() => {
        fetch('http://localhost:8081/api/tickers')
            .then(response => response.json())
            .then(data => {
                console.log("Tickers fetched:", data);
                const options = (data.content || []).map(ticker => ({
                    value: ticker.tickerId, // Unique value
                    label: ticker.tickerName, // Display name
                }));
                setTickers(options); // Set options for dropdown // Extract content property
            })
            .catch(error => console.error("Error fetching tickers:", error));

    }, []);


    const handleTickerChange = (selectedOption) => {
        setSelectedTicker(selectedOption);

        // Send POST request to backend
        axios
            .post('http://127.0.0.1:5001/predict', { ticker: selectedOption.value })
            .then(response => {
                const data = response.data;

                // Update state with chart data and prediction
                setFinalPrediction(data.final_prediction);
                setChartData({
                    labels: Array.from({ length: data.actual_prices.length }, (_, i) => i + 1),
                    datasets: [
                        {
                            label: 'Actual Prices',
                            data: data.actual_prices,
                            borderColor: 'blue',
                            fill: false,
                        },
                        {
                            label: 'Predicted Prices',
                            data: data.predicted_prices,
                            borderColor: 'green',
                            fill: false,
                        },
                    ],
                });
            })
            .catch(error => {
                console.error('Error fetching predictions:', error.response?.data || error.message);
            });
    };


    return (
        <div>
            <h1>Stock Price Predictions</h1>

            <Select
                options={tickers}
                onChange={handleTickerChange}
                placeholder="Select a Ticker"
            />
            {selectedTicker && <h2>Selected Ticker: {selectedTicker.label}</h2>}
            {chartData && (
                <div style={{ width: "80%", height: "400px", margin: "auto" }}>
                    <Line
                        data={chartData}
                        options={{
                            responsive: true,
                            maintainAspectRatio: false,
                        }}
                    />
                </div>
            )}
            {finalPrediction && <h3>Final Predicted Price: ${finalPrediction.toFixed(2)}</h3>}
        </div>
    );
};

export default Predictions;
