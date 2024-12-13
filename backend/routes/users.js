const express = require('express');
const { signUp, login, getCurrentUser, verifyOtp, resendOtp } = require('../controllers/users');
const authenticateToken = require('../middleware/authenticateToken');
const router = express.Router();

// Rute pengguna
router.post('/signup', signUp);
router.post('/login', login);
router.get('/me', authenticateToken, getCurrentUser);
router.post('/verify-otp', verifyOtp);  // Endpoint untuk verifikasi OTP
router.post('/resend-otp', resendOtp);  // Endpoint untuk mengirim ulang OTP

module.exports = router;
