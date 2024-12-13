const User = require('../models/user');

// Halaman utama (Home Page) setelah login
exports.getHomePage = async (req, res) => {
    const userId = req.user.userId;

    try {
        const user = await User.findByPk(userId);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        // Mengembalikan data homepage dengan menyertakan username dan foto profil (default)
        res.status(200).json({
            message: `Welcome, ${user.username}`,
            profile_image: user.profile_image || 'default.jpg', // Foto profil default
        });
    } catch (err) {
        res.status(500).json({ error: 'Failed to load homepage' });
    }
};

exports.getBalance = async (req, res) => {
    const userId = req.user.userId;  // ID user diambil dari token JWT

    try {
        const user = await User.findByPk(userId);  // Cari user berdasarkan ID
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Format saldo menjadi IDR
        const formattedBalance = new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
        }).format(user.balance);

        // Kirimkan response dengan data saldo yang terformat
        res.status(200).json({
            message: 'User balance retrieved successfully',
            balance: formattedBalance
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to retrieve balance' });
    }
};

