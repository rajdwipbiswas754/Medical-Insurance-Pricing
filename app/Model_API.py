from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import pickle
import csv
import os
import datetime
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor

MODEL_PATH = "insurancemodelf.pkl"
LOG_FILE = "log.csv"
HTML_FILE = "index.html"

# -----------------------------
# Load model
# -----------------------------
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# -----------------------------
# Prediction function
# -----------------------------
def predict_price(data):
    features = model.feature_names_in_
    X = [[data[f] for f in features]]
    return float(model.predict(X)[0])


# -----------------------------
# Setup CSV log
# -----------------------------
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp"] + list(model.feature_names_in_) + ["prediction"])

init_log()


# -----------------------------
# Request handler
# -----------------------------
class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            with open(HTML_FILE, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path != "/predict":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(length)
        data = json.loads(body)

        input_data = data["data"]
        prediction = predict_price(input_data)

        # Log request
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [datetime.datetime.now()] +
                [input_data[f] for f in model.feature_names_in_] +
                [prediction]
            )

        # Send JSON response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"predicted_price": prediction}).encode())


# -----------------------------
# Run server
# -----------------------------
def run():
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Server running on port 8000...")
    server.serve_forever()


if __name__ == "__main__":
    run()
