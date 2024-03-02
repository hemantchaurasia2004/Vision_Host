import KalmanFilter from 'kalmanjs';
// import noble from 'noble';

import express from 'express';
import bodyParser from 'body-parser';

// const express = require('express');
// const bodyParser = require('body-parser');
// const KalmanFilter = require('kalmanjs').default;

const app = express();
const port = 3000;

// Create a Kalman filter instance for RSSI values
const kalmanFilter = new KalmanFilter();

// Middleware to parse JSON requests
app.use(bodyParser.json());

// Endpoint to receive real-time RSSI values and return filtered results
app.post('/api/filter-rssi', (req, res) => {
    const { rssi } = req.body;

    // Apply Kalman filter to the RSSI value
    const filteredRssi = kalmanFilter.filter(rssi);

    // You can perform additional processing or store the data in a database here

    // Return the filtered RSSI value
    res.json({ filteredRssi });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
