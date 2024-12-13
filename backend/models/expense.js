const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Expense = sequelize.define('Expense', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    user_id: {
        type: DataTypes.INTEGER,
        allowNull: false
    },
    Amount: {
        type: DataTypes.DECIMAL(10, 2),
        allowNull: false
    },
    Category: {
        type: DataTypes.STRING,
        allowNull: false
    },
    Date: {
        type: DataTypes.DATEONLY,  // Menggunakan hanya tanggal
        allowNull: false
    },
    Mode: {  
        type: DataTypes.STRING,
        allowNull: false,
        defaultValue: 'Cash'  
    },
    Subcategory: {  
        type: DataTypes.STRING,
        allowNull: false,
        defaultValue: 'Unknown'  
    },
    Note: {  
        type: DataTypes.STRING,
        allowNull: true,
        defaultValue: ''  
    },
    Currency: {  
        type: DataTypes.STRING,
        allowNull: false,
        defaultValue: 'IDR'  
    },
    // Menambahkan kolom Expense dengan nilai default "Expense"
    Expense: {
        type: DataTypes.INTEGER,
        allowNull: false,
        defaultValue: '1'  // Nilai default untuk kolom ini
    }
}, {
    timestamps: true,
    freezeTableName: true 
});

module.exports = Expense;
