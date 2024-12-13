const { Op } = require('sequelize');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/user'); // Mengimpor model User
const nodemailer = require('nodemailer'); // Untuk mengirim email OTP
const crypto = require('crypto'); // Untuk membuat OTP

// Fungsi untuk mengirim OTP melalui email
async function sendOtpEmail(email_or_phone, otp) {
    const transporter = nodemailer.createTransport({
        service: 'gmail', // Ganti dengan penyedia email yang digunakan
        auth: {
            user: process.env.EMAIL_USER, // Email pengirim
            pass: process.env.EMAIL_PASS, // Password email pengirim
        },
    });

    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: email_or_phone,
        subject: 'Your OTP Code for Email Verification',
        text: `Your OTP code is: ${otp}`,
    };

    try {
        await transporter.sendMail(mailOptions);
    } catch (error) {
        console.error('Error sending OTP email:', error);
    }
}

// Fungsi untuk membuat OTP random 4 digit
function generateOtp() {
    return Math.floor(1000 + Math.random() * 9000); // OTP 4 digit
}

// Sign Up
exports.signUp = async (req, res) => {
    const { username, email_or_phone, password, confirmPassword, full_name, date_of_birth } = req.body;
  
    // Validasi input
    if (!username || !email_or_phone || !password || !confirmPassword || !full_name || !date_of_birth) {
      return res.status(400).json({ error: 'All fields are required' });
    }
  
    // Pastikan password dan confirm password cocok
    if (password !== confirmPassword) {
      return res.status(400).json({ error: 'Passwords do not match' });
    }
  
    // Cek apakah email_or_phone sudah terdaftar
    const existingUser = await User.findOne({
      where: {
        email_or_phone: email_or_phone, // Cek jika email_or_phone sudah ada
      }
    });
  
    if (existingUser) {
      return res.status(400).json({ error: 'Email or phone number already exists' });
    }
  
    // Format tanggal lahir ke format YYYY-MM-DD
    const [day, month, year] = date_of_birth.split('/');
    const formattedDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
  
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
  
    // Simpan pengguna baru ke database
    try {
      const newUser = await User.create({
        username,
        email_or_phone, // Simpan email_or_phone sebagai nilai untuk email atau nomor telepon
        password_hash: hashedPassword,
        full_name,
        date_of_birth: formattedDate, // Menyimpan tanggal lahir dengan format YYYY-MM-DD
      });
  
      // Generate OTP
      const otp = generateOtp();
  
      // Simpan OTP di database atau memory cache untuk sementara
      newUser.otp = otp;
      newUser.otpExpiry = Date.now() + 15 * 60 * 1000; // OTP kadaluarsa dalam 15 menit
      await newUser.save();
  
      // Kirim OTP melalui email
      await sendOtpEmail(email_or_phone, otp);
  
      res.status(201).json({ message: 'User created, OTP sent to email or phone' });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Error saving user to database' });
    }
};

// Verify OTP
exports.verifyOtp = async (req, res) => {
    const { email_or_phone, otp } = req.body;
  
    // Cari pengguna berdasarkan email_or_phone
    const user = await User.findOne({ where: { email_or_phone: email_or_phone } });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
  
    // Cek apakah OTP sesuai dan belum kadaluarsa
    if (user.otp === parseInt(otp) && Date.now() < user.otpExpiry) {
      // OTP valid, buat token dan kirimkan ke pengguna
      const token = jwt.sign(
        { userId: user.id, username: user.username },
        process.env.JWT_SECRET,
        { expiresIn: '1h' }  // Sesuaikan waktu expired jika perlu
      );

      res.status(200).json({ 
        message: 'OTP verified successfully',
        token: token  // Kirimkan token kembali
      });
    } else {
      res.status(400).json({ error: 'Invalid or expired OTP' });
    }
};

// Resend OTP (mengirim ulang OTP)
exports.resendOtp = async (req, res) => {
    const { email_or_phone } = req.body;

    // Cari pengguna berdasarkan email_or_phone
    const user = await User.findOne({ where: { email_or_phone: email_or_phone } });
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }

    // Cek apakah OTP sudah kadaluarsa
    if (Date.now() > user.otpExpiry) {
        // Generate OTP baru
        const otp = generateOtp();

        // Perbarui OTP dan waktu kadaluarsa
        user.otp = otp;
        user.otpExpiry = Date.now() + 15 * 60 * 1000; // 15 menit kadaluarsa
        await user.save();

        // Kirim OTP melalui email
        await sendOtpEmail(email_or_phone, otp);

        res.status(200).json({ message: 'OTP has been resent to email' });
    } else {
        res.status(400).json({ error: 'OTP is still valid. Please check your email' });
    }
};

// Login
exports.login = async (req, res) => {
    const { email_or_phone, password } = req.body;

    // Cari pengguna berdasarkan email_or_phone
    const user = await User.findOne({ where: { email_or_phone: email_or_phone } });
    if (!user) {
        return res.status(401).json({ error: 'User not found' });
    }

    // Verifikasi password
    const isPasswordValid = await bcrypt.compare(password, user.password_hash);
    if (!isPasswordValid) {
        return res.status(401).json({ error: 'Invalid password' });
    }

    // Buat JWT token
    const token = jwt.sign(
        { userId: user.id, username: user.username },
        process.env.JWT_SECRET,
        { expiresIn: '1h' }
    );

    res.status(200).json({ message: 'Login successful', token });
};

// Get Current User
exports.getCurrentUser = async (req, res) => {
    const user = await User.findByPk(req.user.userId);
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }

    res.status(200).json({
        userId: user.id,
        username: user.username,
        email_or_phone: user.email_or_phone,
        full_name: user.full_name,
        date_of_birth: user.date_of_birth,
    });
};
