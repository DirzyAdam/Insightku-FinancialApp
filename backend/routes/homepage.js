const express = require('express');
const { getHomePage, getBalance } = require('../controllers/homepage');
const authenticateToken = require('../middleware/authenticateToken');
const router = express.Router();

// Route untuk homepage (berisi welcome dan profil)
router.get('/', authenticateToken, getHomePage);

// Route untuk mengambil saldo pengguna
router.get('/balance', authenticateToken, getBalance);

module.exports = router;
