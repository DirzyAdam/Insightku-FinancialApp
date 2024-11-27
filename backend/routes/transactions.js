const express = require('express');
const { getTransactions, addTransaction } = require('../controllers/transactions');
const router = express.Router();

router.get('/', getTransactions); // Get all transactions
router.post('/', addTransaction); // Add a transaction

module.exports = router;
