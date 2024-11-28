# Insightku API - Backend

**Insightku API** adalah backend untuk aplikasi yang menyediakan fitur manajemen pengguna, termasuk pendaftaran, login, dan pengelolaan data pengguna dengan otentikasi berbasis JWT (JSON Web Token). API ini menggunakan **Express.js** sebagai framework utama, **bcrypt** untuk enkripsi password, dan **jsonwebtoken** untuk mengelola token autentikasi. Data pengguna disimpan sementara di **in-memory storage** (data disimpan sementara di memori, bukan di database).

## endpoint (sementara):
- **Sign Up**: Pengguna dapat mendaftar dengan email, username, dan password.
- **Login**: Pengguna dapat masuk dengan email dan password untuk mendapatkan token JWT.
- **Get Current User**: Pengguna dapat mengambil data mereka sendiri setelah berhasil login menggunakan token JWT.
- **Protected Route**: Hanya pengguna dengan token yang valid yang dapat mengakses rute yang dilindungi.

## Teknologi yang Digunakan:
- **Node.js** 
- **Express.js** untuk membangun REST API
- **bcrypt** untuk enkripsi password
- **jsonwebtoken** untuk autentikasi menggunakan token JWT
- **dotenv** untuk mengelola variabel lingkungan

## Cara Menggunakan

### 1. Clone repository:
Clone repository ini ke mesin lokal Anda:
```bash
git clone https://github.com/username/insightku-backend.git
cd insightku-backend
