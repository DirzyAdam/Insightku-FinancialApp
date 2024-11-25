const db = require('../config/db');

// Get all transactions
exports.getTransactions = async (req, res) => {
    try {
        const [rows] = await db.query('SELECT * FROM Transactions');
        res.status(200).json(rows);
    } catch (error) {
        res.status(500).json({ message: "Error fetching transactions", error });
    }
};

// Add a transaction
exports.addTransaction = async (req, res) => {
    const { user_id, type, category, amount, transaction_date, notes } = req.body;
    try {
        const [result] = await db.query(
            'INSERT INTO Transactions (user_id, type, category, amount, transaction_date, notes) VALUES (?, ?, ?, ?, ?, ?)',
            [user_id, type, category, amount, transaction_date, notes]
        );
        res.status(201).json({ message: "Transaction added", transaction_id: result.insertId });
    } catch (error) {
        res.status(500).json({ message: "Error adding transaction", error });
    }
};
