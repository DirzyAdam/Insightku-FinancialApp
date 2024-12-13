const { DataTypes } = require('sequelize');
const sequelize = require('../config/database'); // Mengimpor konfigurasi database
const Expense = require('./expense');
const Goal = require('./goals');

const User = sequelize.define('User', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {
    type: DataTypes.STRING,
    allowNull: false
  },
  email_or_phone: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  password_hash: {
    type: DataTypes.STRING,
    allowNull: false
  },
  full_name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  date_of_birth: {
    type: DataTypes.DATEONLY, // Format tanggal untuk YYYY-MM-DD
    allowNull: false
  },
  otp: {
    type: DataTypes.INTEGER, // OTP berupa angka
    allowNull: true
  },
  otpExpiry: {
    type: DataTypes.DATE,
    allowNull: true
  },
  // Kolom baru yang ditambahkan
  profile_picture: {
    type: DataTypes.STRING, // Menyimpan URL atau path foto profil
    allowNull: true
  },
  dark_theme: {
    type: DataTypes.BOOLEAN, // Menyimpan status mode gelap
    defaultValue: false
  },
  push_notification: {
    type: DataTypes.BOOLEAN, // Menyimpan status notifikasi push
    defaultValue: true
  },
  balance: {
    type: DataTypes.DECIMAL(10, 2),  // Kolom balance untuk menyimpan saldo
    allowNull: false,
    defaultValue: 0.00  // Default saldo adalah 0
  },
  // Pengaturan notifikasi
  generalNotification: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  sound: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  soundCall: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  vibrate: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  }
}, {
  timestamps: true,
  freezeTableName: true  // Menambahkan kolom createdAt dan updatedAt
});

User.hasMany(Goal, { foreignKey: 'user_id' });
User.hasMany(Expense, { foreignKey: 'user_id' });  // Relasi satu ke banyak (one-to-many)
Expense.belongsTo(User, { foreignKey: 'user_id' });  // Relasi sebaliknya

module.exports = User;
