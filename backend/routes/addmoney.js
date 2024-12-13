const express = require('express');
const { addMoney } = require('../controllers/addmoney');
const authenticateToken = require('../middleware/authenticateToken');
const router = express.Router();

// Rute untuk menambahkan uang
router.post('/add', authenticateToken, addMoney);

module.exports = router;
