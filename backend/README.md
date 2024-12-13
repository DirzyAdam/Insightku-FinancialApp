# Insightku API - Backend Cloud Computing

**Insightku API** Google Cloud Platform (GCP) is a suite of cloud computing services provided by Google that enables businesses and developers to run applications, manage data, and build software solutions in a scalable and secure environment. GCP offers a wide range of services for computing, storage, machine learning, and more, allowing users to leverage Google's infrastructure and technology for various cloud-based tasks.

## Here are the services used in this project:

- **Cloud Storage**: Used for storing SQL model tables and other necessary data.
- **App Engine**: Deployed to host the backend API and the Flask API (model).
- **Cloud SQL**: Serves as the relational database for managing structured data.

## endpoint (sementara):
- **Sign Up**: Pengguna dapat mendaftar dengan email, username, dan password.
- **Login**: Pengguna dapat masuk dengan email dan password untuk mendapatkan token JWT.
- **Get Current User**: Pengguna dapat mengambil data mereka sendiri setelah berhasil login menggunakan token JWT.
- **Protected Route**: Hanya pengguna dengan token yang valid yang dapat mengakses rute yang dilindungi.


## Cara Menggunakan

### 1. Clone repository:
Clone repository ini ke mesin lokal Anda:
```bash
git clone https://github.com/DirzyAdam/Insightku-FinancialApp.git
cd Insightku-FinancialApp/backend
```

```bash
npm run start
```

### Tes Endpoint 
- **sign up (post)** : http://localhost:5000/api/users/signup
```
{
  "username": "newUser",
  "email": "newuser@example.com",
  "password": "securePassword123"
}
```
- **login (post)** : http://localhost:5000/api/users/login
```
{
  "email": "newuser@example.com",
  "password": "securePassword123"
}
```
```
{
  "message": "Login successful",
  "token": "your_jwt_token_here"
}
```
- **akses data (get)** : http://localhost:5000/api/users/me
Pada tab Headers, tambahkan header berikut:
- Key: Authorization
- Value: Bearer your_jwt_token_here (ganti dengan token yang Anda dapatkan dari login).
- kalo valid, respons :
```
{
  "userId": 0,
  "username": "newUser",
  "email": "newuser@example.com"
}
```
