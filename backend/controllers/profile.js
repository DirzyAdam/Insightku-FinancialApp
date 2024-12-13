const User = require('../models/user');
const bcrypt = require('bcrypt');

// Halaman profil pengguna
exports.getProfilePage = async (req, res) => {
    const userId = req.user.userId;

    try {
        const user = await User.findByPk(userId);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        // Mengembalikan data profil pengguna
        res.status(200).json({
            username: user.username,
            full_name: user.full_name,
            email_or_phone: user.email_or_phone,
            date_of_birth: user.date_of_birth,
            profile_image: user.profile_image || 'default.jpg', // Foto profil, jika tidak ada, gunakan default
        });
    } catch (err) {
        res.status(500).json({ error: 'Failed to load profile page' });
    }
};

// Fungsi untuk memperbarui profil pengguna
exports.updateProfile = async (req, res) => {
    const { username, email_or_phone, full_name, date_of_birth, profile_picture, dark_theme, push_notification } = req.body;
    
    // Validasi input
    if (!username || !email_or_phone || !full_name || !date_of_birth) {
      return res.status(400).json({ error: 'Username, email, full name, and date of birth are required.' });
    }
  
    try {
      // Cari pengguna berdasarkan ID (ID ada di token)
      const user = await User.findByPk(req.user.userId);
      if (!user) {
        return res.status(404).json({ error: 'User not found.' });
      }
  
      // Perbarui data pengguna
      user.username = username;
      user.email_or_phone = email_or_phone;
      user.full_name = full_name;
      user.date_of_birth = date_of_birth;
      if (profile_picture) user.profile_picture = profile_picture;
      user.dark_theme = dark_theme;
      user.push_notification = push_notification;
  
      await user.save(); // Simpan perubahan ke database
  
      res.status(200).json({ message: 'Profile updated successfully.' });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Error updating profile.' });
    }
  };
  

// Logout - Menghapus token untuk logout
exports.logout = (req, res) => {
    // Cukup hapus token di sisi client, atau bisa dengan menonaktifkan session
    res.status(200).json({ message: 'Logged out successfully' });
};

// Fungsi untuk mengganti password pengguna
exports.changePassword = async (req, res) => {
    const { currentPassword, newPassword, confirmPassword } = req.body;
    const userId = req.user.userId;

    // Validasi input
    if (!currentPassword || !newPassword || !confirmPassword) {
        return res.status(400).json({ error: 'Current password, new password, and confirm password are required' });
    }

    if (newPassword !== confirmPassword) {
        return res.status(400).json({ error: 'New password and confirm password do not match' });
    }

    try {
        // Cari pengguna berdasarkan ID
        const user = await User.findByPk(userId);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Verifikasi apakah currentPassword cocok dengan password yang disimpan
        const isPasswordValid = await bcrypt.compare(currentPassword, user.password_hash);
        if (!isPasswordValid) {
            return res.status(401).json({ error: 'Current password is incorrect' });
        }

        // Hash password baru
        const hashedNewPassword = await bcrypt.hash(newPassword, 10);

        // Update password di database
        user.password_hash = hashedNewPassword;
        await user.save();

        res.status(200).json({ message: 'Password successfully changed' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Failed to change password' });
    }
};

exports.notifications = async (req, res) => {
    const { generalNotification, sound, soundCall, vibrate } = req.body;
    
    if (generalNotification === undefined || sound === undefined || soundCall === undefined || vibrate === undefined) {
        return res.status(400).json({ error: 'All notification settings are required' });
    }

    try {
        // Cari pengguna berdasarkan ID (ID ada di token)
        const user = await User.findByPk(req.user.userId);
        if (!user) {
            return res.status(404).json({ error: 'User not found.' });
        }

        // Perbarui pengaturan notifikasi pengguna
        user.generalNotification = generalNotification;
        user.sound = sound;
        user.soundCall = soundCall;
        user.vibrate = vibrate;

        await user.save(); // Simpan perubahan ke database

        res.status(200).json({ message: 'Notification settings updated successfully.' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error updating notification settings.' });
    }
};