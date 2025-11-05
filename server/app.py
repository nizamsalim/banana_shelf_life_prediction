from flask import Flask,jsonify,request
from model import SpoilagePredictionModel
from database import SpoilageRecord,db
from os import path,makedirs,remove
from PIL import Image
import io
import uuid
import requests
import os

app = Flask(__name__)
obj = SpoilagePredictionModel("banana_spoilage_mobilenet.h5")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


UPLOADS_DIR="uploads"
makedirs(UPLOADS_DIR,exist_ok=True)

def get_sensor_data():
    FIREBASE_URL = os.environ.get("FIREBASE_URL")

    response = requests.get(FIREBASE_URL)
    data = response.json()

    # Sort timestamps descending (latest first)
    timestamps = sorted(data.keys(), reverse=True)

    # Pick last 3 readings
    last_3 = {ts: data[ts] for ts in timestamps[:3]}

    latest_data = data[timestamps[0]]

    return latest_data.get("temperature"),latest_data.get("humidity"),latest_data.get("alcohol")

@app.route("/upload",methods=["POST"])
def handle_data_upload():
    try:
        temperature, humidity, ethylene = get_sensor_data()

        # ✅ Check if an image file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']

        # ✅ Validate file
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        print(file)

        # ✅ Create unique ID and save file temporarily
        record_id = uuid.uuid4()
        filename = path.join(UPLOADS_DIR, f"{record_id}.jpeg")
        file.save(filename)

        # ✅ Process image
        response = obj.get_shelf_life(filename, temperature, humidity, ethylene)

        data = {
            "id": str(record_id),
            "stage": response["stage"],
            "temperature": response["input"]["temperature"],
            "humidity": response["input"]["humidity"],
            "ethylene": response["input"]["ethylene"],
            "shelf_life_min": response["min_days"],
            "shelf_life_max": response["max_days"],
            "shelf_life_median": response["median_days"]
        }

        record = SpoilageRecord(**data)
        db.session.add(record)
        db.session.commit()

        # os.remove(filename)
        return jsonify(data), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route("/data",methods=["GET"])
def get_latest_data():
    print("flag")
    latest_record = SpoilageRecord.query.order_by(SpoilageRecord.created_at.desc()).first()
    if latest_record:
        return jsonify(latest_record.to_dict())
    return {"error":"No data found"},404

if __name__ == "__main__":
    app.run(debug=True,port=3000)