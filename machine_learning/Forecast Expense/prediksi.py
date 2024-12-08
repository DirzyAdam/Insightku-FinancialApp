import requests
import json
import numpy as np
from datetime import datetime

# Contoh data historis (minimal 15 hari)
data = [
    {
        "Date": "2024-03-01",
        "Mode": "afk",
        "Category": "Food",
        "Subcategory": "Afuy",
        "Amount": 500,
        "Note": "Cihuy",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-02",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Dinner",
        "Amount": 750,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-03",
        "Mode": "Cash",
        "Category": "Transportation",
        "Subcategory": "Taxi",
        "Amount": 3500,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-04",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Lunch",
        "Amount": 400,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-05",
        "Mode": "Cash",
        "Category": "Utilities",
        "Subcategory": "Lunch",
        "Amount": 200,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-06",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Lunch",
        "Amount": 5500,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-07",
        "Mode": "Cash",
        "Category": "Entertainment",
        "Subcategory": "Lunch",
        "Amount": 1000,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-08",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Dinner",
        "Amount": 800,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-09",
        "Mode": "Cash",
        "Category": "Transportation",
        "Subcategory": "Lunch",
        "Amount": 15,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-10",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Lunch",
        "Amount": 450,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-11",
        "Mode": "Cash",
        "Category": "Shopping",
        "Subcategory": "Lunch",
        "Amount": 3000,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-12",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Dinner",
        "Amount": 7000,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-13",
        "Mode": "Cash",
        "Category": "Utilities",
        "Subcategory": "Lunch",
        "Amount": 2500,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-14",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Lunch",
        "Amount": 6000,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
    {
        "Date": "2024-03-15",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Dinner",
        "Amount": 1200,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    },
        {
        "Date": "2024-03-16",
        "Mode": "Cash",
        "Category": "Food",
        "Subcategory": "Lunch",
        "Amount": 1500,
        "Note": "",
        'Expense': 1,
        "Currency": "IDR"
    }
]

# Kirim request
url = 'http://localhost:5000/predict'
response = requests.post(url, json=data)

# Periksa respons
if response.status_code == 200:
    predictions = response.json()['predictions']
    
    # Tampilkan prediksi
    for prediction in predictions:
        print(f"Tanggal: {prediction['Date']}, Prediksi Pengeluaran: {prediction['Predicted_Amount']} IDR")
else:
    print("Error:", response.json())