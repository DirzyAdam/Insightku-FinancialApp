const express = require('express');
const { addGoals, getGoals, getRecentGoals } = require('../controllers/goals');
const authenticateToken = require('../middleware/authenticateToken'); // Middleware untuk otentikasi
const router = express.Router();

// Rute untuk menambahkan uang
router.post('/add', authenticateToken, addGoals);

// Rute untuk mendapatkan semua goals
router.get('/', authenticateToken, getGoals);

// Rute untuk mendapatkan recent goals (goal terbaru)
router.get('/recent', authenticateToken, getRecentGoals);

module.exports = router;
