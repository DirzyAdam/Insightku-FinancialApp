const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const dotenv = require('dotenv');

// Import rute dan middleware
const userRoutes = require('./routes/users');
const homepageRoutes = require('./routes/homepage');  // Rute untuk homepage
const profileRoutes = require('./routes/profile');    // Rute untuk profil pengguna
const addMoneyRoutes = require('./routes/addmoney');  // Rute untuk menambahkan uang
const expenseRoutes = require('./routes/expense');  // Rute untuk pengeluaran
const goalsRoutes = require('./routes/goals');  // Rute untuk goals
const authenticateToken = require('./middleware/authenticateToken'); // Middleware otentikasi
const sequelize = require('./config/database');  // Koneksi database

dotenv.config();

const app = express();

// Middleware global
app.use(cors());
app.use(bodyParser.json());

// Rute utama
app.use('/api/users', userRoutes);          // Rute untuk pengguna (sign up, login, dll)
app.use('/api/home', authenticateToken, homepageRoutes);  // Rute untuk halaman utama (homepage)
app.use('/api/home/profile', authenticateToken, profileRoutes);  // Rute untuk halaman profil pengguna
app.use('/api/home/add-money', authenticateToken, addMoneyRoutes);  // Rute untuk menambahkan uang
app.use('/api/expenses', authenticateToken, expenseRoutes);  // Rute untuk pengeluaran
app.use('/api/goals', authenticateToken, goalsRoutes); // Rute untuk goals

// Rute terproteksi (Contoh, bisa disesuaikan untuk kebutuhan lainnya)
app.get('/api/protected', authenticateToken, (req, res) => {
    res.status(200).json({ message: 'This is a protected route', user: req.user });
});

// Sinkronisasi database
sequelize.sync()
  .then(() => {
    console.log('Database synchronized');
  })
  .catch((err) => {
    console.error('Error syncing database:', err);
  });

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
