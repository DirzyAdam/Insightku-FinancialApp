const User = require('../models/user');
const Goal = require('../models/goals');

// Fungsi untuk menambahkan goal
exports.addGoals = async (req, res) => {
    const { goal_name, goal_amount, goal_color } = req.body;
    const userId = req.user.userId;  // Ambil userId dari token

    // Validasi input
    if (!goal_name || !goal_amount || goal_amount <= 0) {
        return res.status(400).json({ error: 'All fields are required and goal_amount must be greater than 0' });
    }

    try {
        // Cek apakah user ada di database
        const user = await User.findByPk(userId);  // Gunakan userId yang benar

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        // Menambahkan goal ke database
        const newGoal = await Goal.create({
            user_id: userId,  // Gunakan userId yang benar
            goal_name,
            goal_amount,
            goal_color
        });

        // Menambahkan respons dengan informasi goal baru
        res.status(201).json({
            message: 'Goal added successfully',
            goal: newGoal
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Error adding goal', error: err });
    }
};

// Mendapatkan semua goals milik user
exports.getGoals = async (req, res) => {
    const userId = req.user.userId;   // Ambil user_id dari token
  
    try {
        const goals = await Goal.findAll({
            where: { user_id: userId }
        });
  
        // Total jumlah goal yang sudah dicapai
        let totalAmount = goals.reduce((acc, goal) => acc + parseFloat(goal.goal_amount), 0);
  
        // Menambahkan persentase untuk setiap goal dan hanya mengirimkan data yang diperlukan
        const goalsWithPercentage = goals.map(goal => {
            const percentage = (parseFloat(goal.goal_amount) / totalAmount) * 100;
            return {
                goal_name: goal.goal_name,   // Menampilkan hanya goal_name
                percentage: percentage.toFixed(2)  // Format persentase dengan dua angka di belakang koma
            };
        });
  
        // Kirimkan totalAmount dan goals dengan persentase
        res.status(200).json({ 
            totalAmount,  // Menampilkan total jumlah goal yang dicapai
            goals: goalsWithPercentage  // Menampilkan goal_name dan persentase
        });
    } catch (err) {
        res.status(500).json({ message: 'Error retrieving goals', error: err });
    }
};

// Mendapatkan recent goals (goal terbaru berdasarkan waktu)
exports.getRecentGoals = async (req, res) => {
    const userId = req.user.userId;  // Ambil user_id dari token

    try {
        const recentGoals = await Goal.findAll({
            where: { user_id: userId },
            order: [['createdAt', 'DESC']],  // Urutkan berdasarkan createdAt terbaru
            limit: 5  // Menampilkan 5 goal terbaru, bisa disesuaikan
        });

        // Total jumlah goal yang sudah dicapai
        let totalAmount = recentGoals.reduce((acc, goal) => acc + parseFloat(goal.goal_amount), 0);

        // Menambahkan persentase untuk setiap goal dan hanya mengirimkan data yang diperlukan
        const recentGoalsWithPercentage = recentGoals.map(goal => {
            const percentage = (parseFloat(goal.goal_amount) / totalAmount) * 100;
            return {
                goal_name: goal.goal_name,   // Menampilkan goal_name
                goal_amount: goal.goal_amount, // Menampilkan goal_amount
                percentage: percentage.toFixed(2)  // Format persentase dengan dua angka di belakang koma
            };
        });

        res.status(200).json({
            recentGoals: recentGoalsWithPercentage  // Menampilkan goal_name, goal_amount dan persentase 
        });
    } catch (err) {
        res.status(500).json({ message: 'Error retrieving recent goals', error: err });
    }
};

