from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        prices = data.get("prices", [])
        method = data.get("method", "linear-regression")

        if not isinstance(prices, list) or len(prices) < 5:
            return jsonify({"error": "At least 5 closing prices required"}), 400

        # Method: average
        if method == "average":
            avg_price = round(sum(prices[-10:]) / min(10, len(prices)), 2)
            return jsonify({"predicted_price": avg_price})

        # Method: linear-regression
        elif method == "linear-regression":
            X = np.arange(len(prices)).reshape(-1, 1)
            y = np.array(prices).reshape(-1, 1)

            model = LinearRegression()
            model.fit(X, y)

            next_day = np.array([[len(prices)]])
            prediction = model.predict(next_day)[0][0]

            return jsonify({"predicted_price": round(float(prediction), 2)})

        else:
            return jsonify({"error": "Invalid method"}), 400

    except Exception as e:
        print("🔥 Error in prediction:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
