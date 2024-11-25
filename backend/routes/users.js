const express = require('express');
const { signUp, login, getCurrentUser } = require('../controllers/users');
const authenticateToken = require('../middleware/authenticateToken');
const router = express.Router();

// Rute pengguna
router.post('/signup', signUp);
router.post('/login', login);
router.get('/me', authenticateToken, getCurrentUser);

module.exports = router;
