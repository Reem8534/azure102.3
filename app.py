from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import os

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""
    LOG.info("Scaling Payload: \n%s", payload)
    scaler = StandardScaler().fit(payload)
    scaled_adhoc_predict = scaler.transform(payload)
    return scaled_adhoc_predict

@app.route("/")
def home():
    return "<h3>Sklearn Prediction Home</h3>"

@app.route("/predict", methods=['POST'])
def predict():
    try:
        model_path = "./Housing_price_model/LinearRegression.joblib"
        if not os.path.exists(model_path):
            return jsonify({"error": "Model file not found"}), 404

        clf = joblib.load(model_path)

        json_payload = request.get_json()
        LOG.info("JSON payload: %s", json_payload)

        inference_payload = pd.DataFrame(json_payload)
        LOG.info("Inference DataFrame: \n%s", inference_payload)

        scaled_payload = scale(inference_payload)
        prediction = list(clf.predict(scaled_payload))
        LOG.info("Prediction: %s", prediction)

        return jsonify({'prediction': prediction})

    except Exception as e:  # pylint: disable=broad-exception-caught
        LOG.error("Error during prediction: %s", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

