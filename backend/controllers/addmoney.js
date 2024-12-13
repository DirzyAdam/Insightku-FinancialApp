const User = require('../models/user');

// Fungsi untuk menambahkan uang ke saldo pengguna
exports.addMoney = async (req, res) => {
    let { amount } = req.body;
    console.log("Received amount: ", amount);  // Debugging: Memastikan nilai amount yang diterima

    if (!amount || amount <= 0) {
        return res.status(400).json({ error: 'Amount must be greater than 0' });
    }

    // Pastikan amount adalah angka dan bersihkan format yang tidak valid (misalnya simbol mata uang)
    amount = parseFloat(amount.toString().replace(/[^\d.-]/g, ''));
    console.log("Parsed amount: ", amount); // Debugging: Cek nilai amount setelah pembersihan

    if (isNaN(amount)) {
        return res.status(400).json({ error: 'Invalid amount format' });
    }

    try {
        const user = await User.findByPk(req.user.userId);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Pastikan balance adalah angka
        user.balance = Number(user.balance);  // Konversi ke angka jika bukan
        user.balance += amount;  // Tambahkan amount ke balance

        // Simpan perubahan saldo
        await user.save();

        console.log("Updated balance: ", user.balance); // Debugging: Cek saldo setelah diupdate

        // Format saldo yang baru
        const formattedBalance = new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
        }).format(user.balance);

        res.status(200).json({
            message: 'Balance added successfully',
            balance: formattedBalance
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error adding money' });
    }
};
