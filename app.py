from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return """
    <html>
      <head>
        <title>Health Check</title>
      </head>
      <body style="font-size: 36px; font-family: Arial, sans-serif; text-align: center; margin-top: 100px;">
        <p>✅ Server is Healthy</p>
        <button onclick="window.location.href='https://ai-stock-prediction-dfv1.onrender.com';" 
                style="padding: 20px 40px; font-size: 28px; background-color: #007BFF; color: white; border: none; border-radius: 8px; cursor: pointer;">
          REDIRECT TO THE MAIN WEBSITE
        </button>
      </body>
    </html>
    """, 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        prices = data.get("prices", [])
        method = data.get("method", "linear-regression")

        if not isinstance(prices, list) or len(prices) < 5:
            return jsonify({"error": "At least 5 closing prices required"}), 400

        X = np.arange(len(prices)).reshape(-1, 1)
        y = np.array(prices).reshape(-1, 1)

        if method == "average":
            avg_price = round(sum(prices[-10:]) / min(10, len(prices)), 2)
            return jsonify({"predicted_price": avg_price})

        elif method == "linear-regression":
            model = LinearRegression()
            model.fit(X, y)
            next_day = np.array([[len(prices)]])
            prediction = model.predict(next_day)[0][0]
            return jsonify({"predicted_price": round(float(prediction), 2)})

        elif method == "polynomial-regression":
            poly = PolynomialFeatures(degree=3)  # degree can be tuned (e.g., 2, 3, 4)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            next_day = poly.transform([[len(prices)]])
            prediction = model.predict(next_day)[0][0]
            return jsonify({"predicted_price": round(float(prediction), 2)})

        else:
            return jsonify({"error": "Invalid method"}), 400

    except Exception as e:
        print("🔥 Error in prediction:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
