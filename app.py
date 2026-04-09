from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
df = pd.read_csv("crop_yield_data.csv")

@app.route("/")
def home():
    return "Crop Yield API Running"

@app.route("/data")
def get_data():
    return df.to_json(orient="records")

@app.route("/summary")
def summary():
    result = df.groupby("Region")["Yield_kg_per_ha"].mean().to_dict()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
