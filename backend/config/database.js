const { Sequelize } = require('sequelize');

const sequelize = new Sequelize({
  host: '34.101.100.201',         
  dialect: 'mysql',
  username: 'root',               
  password: 'Insightku262626',    
  database: 'insightku_db',       
  port: 3306,                     
});

module.exports = sequelize;
