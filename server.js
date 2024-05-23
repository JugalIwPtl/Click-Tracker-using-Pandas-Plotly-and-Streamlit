const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');
const cors = require('cors'); 

const app = express();
const PORT = process.env.PORT || 5500;

app.use(bodyParser.json());
app.use(cors());

app.post('/api/track-click', (req, res) => {
    const clickData = req.body;

    fs.appendFile('click_data.json', JSON.stringify(clickData) + '\n', (err) => {
        if (err) {
            console.error('Error writing click data to file:', err);
            res.status(500).send('Error writing click data to file');
        } else {
            console.log('Click data saved to file:', clickData);
            res.status(200).send('Click data saved successfully');
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
