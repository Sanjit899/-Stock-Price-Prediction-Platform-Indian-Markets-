📈 Stock Price Prediction Platform (Indian Markets)

A full-stack machine learning web application that predicts stock prices for NSE-listed companies using real-time financial data. The platform provides historical price analysis, next-day and 7-day forecasts with visual charts, user authentication, and prediction history storage.

Features

🇮🇳 NSE Stock Selection (Indian companies)

🔐 User Login System

📊 Historical Price Chart (6 months)

📈 7-Day Price Forecast (Visual & Numeric)

🧠 Machine Learning–based Predictions

🗄️ Prediction History Stored in SQLite Database

🛡️ Error Handling for Invalid Stock Symbols

🎨 Clean & Responsive UI

🛠️ Tech Stack

Backend: Python, Flask

Machine Learning: Scikit-learn (Linear Regression)

Data Processing: Pandas, NumPy

Data Source: Yahoo Finance (yfinance)

Visualization: Matplotlib

Database: SQLite

Frontend: HTML, CSS

Authentication: Flask-Login


📂 Project Structure
stock_price_prediction/
│
├── app.py                  # Flask application
├── model.py                # ML model & prediction logic
├── db.py                   # Database initialization
├── predictions.db          # SQLite database
│
├── templates/
│   ├── index.html          # Main app UI
│   └── login.html          # Login page
│
├── static/
│   ├── style.css           # Styling
│   ├── *_chart.png         # Generated price charts
│   └── *_forecast.png      # 7-day forecast charts
│
├── venv/                   # Virtual environment
└── README.md               # Project documentation


⚙️ Installation & Setup (Local)
Create & Activate Virtual Environment
python -m venv venv
Windows :- venv\Scripts\activate
Linux / macOS  :- source venv/bin/activate

Install Dependencies
pip install flask flask-login pandas numpy matplotlib scikit-learn yfinance

Run the Application
Open your browser and visit: http://127.0.0.1:5000

🔐 Default Login Credentials (Demo)

You must create a user before login.

Example:

Username: admin

Password: admin123

📊 How It Works

User logs in to the platform

Selects an NSE stock from the dropdown

Application fetches real-time market data

ML model predicts:

Next-day price

7-day forecast

Results are displayed with visual charts

Prediction history is stored in the database


⚠️ Disclaimer

This project is created for educational and demonstration purposes only.
It should not be used for real financial or trading decisions.


🌟 Future Enhancements

Password hashing & registration system

Prediction history dashboard

Cloud deployment (Render / Railway)

Advanced ML models (LSTM)

Mobile-friendly UI improvements

📜 License

This project is open-source and available for learning and personal use.

