const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

let users = []; // In-memory storage untuk data pengguna

exports.signUp = async (req, res) => {
    const { username, email, password } = req.body;
    if (!username || !email || !password) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    const existingUser = users.find(user => user.email === email);
    if (existingUser) {
        return res.status(400).json({ error: 'Email already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = { username, email, password_hash: hashedPassword };
    users.push(newUser);

    res.status(201).json({ message: 'User created', userId: users.length - 1 });
};

exports.login = async (req, res) => {
    const { email, password } = req.body;
    const user = users.find(user => user.email === email);

    if (!user) {
        return res.status(401).json({ error: 'User not found' });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password_hash);
    if (!isPasswordValid) {
        return res.status(401).json({ error: 'Invalid password' });
    }

    const token = jwt.sign({ userId: users.indexOf(user), username: user.username }, process.env.JWT_SECRET, { expiresIn: '1h' });

    res.status(200).json({ message: 'Login successful', token });
};

exports.getCurrentUser = (req, res) => {
    const user = users[req.user.userId];
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }

    res.status(200).json({ userId: req.user.userId, username: user.username, email: user.email });
};
