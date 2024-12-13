const { Op } = require('sequelize');
const Expense = require('../models/expense');
const User = require('../models/user');
const axios = require('axios');

// Fungsi untuk mengambil data pengeluaran 15 hari terakhir berdasarkan user_id
const getExpensesForPrediction = async (user_id) => {
    try {
        const expenses = await Expense.findAll({
            where: {
                user_id: user_id,
                Date: {
                    [Op.gte]: new Date(new Date() - 15 * 24 * 60 * 60 * 1000), // Mengambil data 15 hari terakhir
                },
            },
            order: [['Date', 'ASC']], // Mengurutkan berdasarkan tanggal
            limit: 15, // Ambil hanya 15 data teratas
        });

        return expenses.map(expense => ({
            Date: expense.Date,
            Mode: expense.Mode,
            Category: expense.Category,
            Subcategory: expense.Subcategory,
            Amount: expense.Amount,
            Note: expense.Note,
            Currency: expense.Currency,
            Expense: expense.Expense || 1 // Menambahkan kolom Expense dengan nilai default 1 jika tidak ada
        }));
    } catch (error) {
        console.error('Error fetching expenses:', error);
        throw new Error('Error fetching expenses');
    }
};


// Fungsi untuk memanggil Flask API dan mendapatkan prediksi pengeluaran
const predictExpenses = async (user_id) => {
    try {
        const expenses = await getExpensesForPrediction(user_id);

        if (expenses.length < 15) {
            throw new Error('Insufficient data for prediction');
        }

        // Ambil tanggal dari transaksi terakhir
        const lastTransactionDate = new Date(expenses[expenses.length - 1].Date);
        
        // Panggil Flask API untuk prediksi pengeluaran
        const response = await axios.post('https://flask-api-dot-insightku-project-443512.et.r.appspot.com/predict', expenses);

        if (response.status === 200 && response.data.predictions) {
            // Format hasil prediksi sesuai yang diinginkan
            const predictions = response.data.predictions.map((prediction, index) => {
                // Setel tanggal mulai dari transaksi terakhir
                const date = new Date(lastTransactionDate);
                date.setDate(lastTransactionDate.getDate() + index + 1); // Prediksi dimulai dari tanggal berikutnya
                return {
                    Date: date.toUTCString(),  // Format UTC
                    Predicted_Amount: prediction.Predicted_Amount || 0 // Pastikan ada Predicted_Amount
                };
            });

            return { predictions };
        } else {
            throw new Error('Failed to get predictions from Flask API');
        }
    } catch (error) {
        console.error('Error during prediction process:', error);
        throw new Error('Prediction failed');
    }
};

// Controller untuk menambah pengeluaran
exports.addExpense = async (req, res) => {
    const { Amount, Category, Date, Mode, Subcategory, Note, Currency } = req.body;
    const userId = req.user.userId;

    // Validasi input
    if (!Amount || Amount <= 0 || !Category || !Date) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    try {
        const user = await User.findByPk(userId);

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        if (user.balance < Amount) {
            return res.status(400).json({ error: 'Insufficient balance' });
        }

        user.balance -= Amount;
        await user.save();

        const expense = await Expense.create({
            user_id: userId,
            Amount,
            Category,
            Date,
            Mode: Mode || 'Cash',
            Subcategory: Subcategory || 'Unknown',
            Note: Note || '',
            Currency: Currency || 'IDR',
            Expense: '1'
        });

        res.status(201).json({
            Amount: expense.Amount,
            Category: expense.Category,
            Date: expense.Date,
            Mode: expense.Mode,
            Subcategory: expense.Subcategory,
            Note: expense.Note,
            Expense: expense.Expense,
            Currency: expense.Currency
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error adding expense' });
    }
};

// Controller untuk mendapatkan total pengeluaran
exports.getTotalExpenses = async (req, res) => {
    const userId = req.user.userId;

    try {
        const expenses = await Expense.findAll({ where: { user_id: userId } });
        const totalExpenses = expenses.reduce((acc, expense) => acc + parseFloat(expense.Amount), 0);

        const user = await User.findByPk(userId);
       
        res.status(200).json({
            message: 'Total expenses retrieved successfully',
            total_expenses: totalExpenses
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Failed to retrieve total expenses' });
    }
};

// Controller untuk mendapatkan transaksi terbaru
exports.getRecentTransactions = async (req, res) => {
    const userId = req.user.userId;

    try {
        const expenses = await Expense.findAll({
            where: { user_id: userId },
            order: [['Date', 'DESC']],
            attributes: ['Amount', 'Category', 'Date', 'Mode', 'Subcategory', 'Note', 'Currency', 'Expense']
        });

        res.status(200).json({
            message: 'Recent transactions retrieved successfully',
            expenses: expenses
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Failed to retrieve recent transactions' });
    }
};

// Controller untuk melakukan prediksi pengeluaran
exports.predictExpenses = async (req, res) => {
    try {
        const { user_id } = req.body;

        if (!user_id) {
            return res.status(400).json({ error: 'user_id is required' });
        }

        // Panggil fungsi prediksi dari controller
        const predictions = await predictExpenses(user_id);

        // Kembalikan hasil prediksi ke client
        return res.json({ predictions: predictions.predictions });
    } catch (error) {
        console.error('Error in prediction route:', error);
        return res.status(500).json({ error: error.message });
    }
};
