const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const dotenv = require('dotenv');

// Import rute dan middleware
const transactionRoutes = require('./routes/transactions');
const userRoutes = require('./routes/users');
const authenticateToken = require('./middleware/authenticateToken'); // Import middleware

dotenv.config();

const app = express();

// Middleware global
app.use(cors());
app.use(bodyParser.json());

// Rute utama
app.use('/api/transactions', transactionRoutes);
app.use('/api/users', userRoutes);

// Rute terproteksi
app.get('/api/protected', authenticateToken, (req, res) => {
    res.status(200).json({ message: 'This is a protected route', user: req.user });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
