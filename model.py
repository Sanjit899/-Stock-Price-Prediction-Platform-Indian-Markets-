import matplotlib
matplotlib.use("Agg")

import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os


def predict_stock_price(symbol):
    try:
        data = yf.download(symbol, period="6mo", auto_adjust=False)

        if data.empty or len(data) < 30:
            return None, None, None, None, "Invalid stock symbol or insufficient data."

        # -----------------------------
        # Feature Engineering
        # -----------------------------
        data['MA5'] = data['Close'].rolling(5).mean()
        data['MA10'] = data['Close'].rolling(10).mean()
        data['MA20'] = data['Close'].rolling(20).mean()

        data['Prediction'] = data['Close'].shift(-1)
        data.dropna(inplace=True)

        X = data[['Close', 'MA5', 'MA10', 'MA20', 'Volume']]
        y = data['Prediction']

        # -----------------------------
        # Train Model
        # -----------------------------
        model = LinearRegression()
        model.fit(X, y)

        current_price = float(data['Close'].iloc[-1].item())

        # -----------------------------
        # 7-Day Forecast
        # -----------------------------
        future_prices = []
        last_features = X.iloc[-1].values.reshape(1, -1)

        for _ in range(7):
            next_price = model.predict(last_features)[0]
            future_prices.append(round(float(next_price), 2))
            last_features[0][0] = next_price  # update Close price

        # -----------------------------
        # Chart Generation (Historical)
        # -----------------------------
        os.makedirs("static", exist_ok=True)

        chart_path = f"static/{symbol}_chart.png"
        plt.figure(figsize=(8, 4))
        plt.plot(data.index, data['Close'], label="Close Price")
        plt.plot(data.index, data['MA20'], label="MA20", linestyle="--")
        plt.legend()
        plt.title(f"{symbol} Price Trend (6 Months)")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

        # -----------------------------
        # 7-Day Forecast Chart
        # -----------------------------
        forecast_chart_path = f"static/{symbol}_forecast.png"

        plt.figure(figsize=(8, 4))
        plt.plot(range(1, 8), future_prices, marker="o")
        plt.title(f"{symbol} 7-Day Forecast")
        plt.xlabel("Days Ahead")
        plt.ylabel("Predicted Price")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(forecast_chart_path)
        plt.close()

        return (
            round(current_price, 2),
            future_prices,
            chart_path,
            forecast_chart_path,
            None
        )

    except Exception as e:
        return None, None, None, None, "Something went wrong. Please try again."
