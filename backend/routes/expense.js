const express = require('express');
const { addExpense, getTotalExpenses, getRecentTransactions, predictExpenses } = require('../controllers/expense');
const authenticateToken = require('../middleware/authenticateToken');
const router = express.Router();

// Route untuk menambah pengeluaran
router.post('/add', authenticateToken, addExpense);

// Route untuk mendapatkan total pengeluaran
router.get('/total', authenticateToken, getTotalExpenses);

// Route untuk mendapatkan transaksi terbaru
router.get('/recent', authenticateToken, getRecentTransactions);

// Route untuk melakukan prediksi pengeluaran
router.post('/predict', authenticateToken, predictExpenses);

module.exports = router;
