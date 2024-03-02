const express = require('express');
const bodyParser = require('body-parser');
const KalmanFilter = require('kalmanjs').default;

const app = express();
const port = 3000;

const kalmanFilter = new KalmanFilter();

app.use(bodyParser.json());

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
