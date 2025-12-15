import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------
# 1. Download stock data
# -------------------------------
stock_symbol = "AAPL"
data = yf.download(stock_symbol, start="2015-01-01", end="2024-12-31")

# -------------------------------
# 2. Feature Engineering
# -------------------------------
data['MA5'] = data['Close'].rolling(window=5).mean()
data['MA10'] = data['Close'].rolling(window=10).mean()
data['MA20'] = data['Close'].rolling(window=20).mean()

# Predict next day close price
data['Prediction'] = data['Close'].shift(-1)

# Remove rows with NaN values
data.dropna(inplace=True)

# Input features
X = data[['Close', 'MA5', 'MA10', 'MA20', 'Volume']]
y = data['Prediction']

# -------------------------------
# 3. Train-Test Split (Time Series)
# -------------------------------
split = int(len(data) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# -------------------------------
# 4. Train Model
# -------------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -------------------------------
# 5. Prediction
# -------------------------------
y_pred = model.predict(X_test)

# -------------------------------
# 6. Evaluation
# -------------------------------
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("📊 Model Performance (With Moving Averages)")
print("Mean Squared Error:", mse)
print("R2 Score:", r2)

# -------------------------------
# 7. Predict Next Day Price
# -------------------------------
last_row = X.iloc[-1].values.reshape(1, -1)
next_day_price = model.predict(last_row)

print(f"\n📈 Predicted Next Day Price for {stock_symbol}: ${next_day_price[0]:.2f}")

# -------------------------------
# 8. Visualization
# -------------------------------
plt.figure(figsize=(10, 5))
plt.plot(y_test.values, label="Actual Price", color="blue")
plt.plot(y_pred, label="Predicted Price", color="red")
plt.legend()
plt.title("Stock Price Prediction with Moving Averages")
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()
