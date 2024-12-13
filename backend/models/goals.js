const { DataTypes } = require('sequelize');
const sequelize = require('../config/database'); // Import database config

const Goal = sequelize.define('Goal', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  goal_name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  goal_amount: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false
  },
  user_id: {
    type: DataTypes.INTEGER,
    allowNull: false,
  },
  goal_color: {
    type: DataTypes.STRING,
    allowNull: true
  }
}, {
  timestamps: true,
});


module.exports = Goal;
