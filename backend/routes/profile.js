const express = require('express');
const { getProfilePage, updateProfile, logout, changePassword, notifications } = require('../controllers/profile');
const authenticateToken = require('../middleware/authenticateToken');
const router = express.Router();

// Route untuk halaman profil pengguna
router.get('/', authenticateToken, getProfilePage);

// Route untuk update profil
router.put('/update', authenticateToken, updateProfile);

// Route untuk logout
router.post('/logout', authenticateToken, logout);

// Route untuk pengaturan
router.post('/settings', authenticateToken, (req, res) => {
  res.status(200).json({ message: 'Settings page accessed' });
});

// Route untuk mengganti password
router.put('/settings/change-password', authenticateToken, changePassword);

router.post('/settings/notification', authenticateToken, notifications);

module.exports = router;
