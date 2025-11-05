# 🍌 AI Powered IoT-based Spoilage & Shelf Life Prediction

A machine learning–driven system for predicting the **shelf life of bananas** using **computer vision and environmental sensor data**.  
This project combines **AI (CNN-based ripeness detection)** and **IoT-based environmental sensing** to estimate and adjust shelf-life predictions dynamically.

---

## 🚀 Features

- 🧠 **Banana Ripeness Classification** — Fine-tuned **MobileNet CNN** model trained on **13,478 images**, classifying bananas into _unripe_, _ripe_, _overripe_, and _rotten_ stages with **98% accuracy**.
- 📊 **Shelf-life Estimation** — Rule-based mapping of each ripeness stage to an initial shelf-life range (e.g., 3–5 days for ripe, 8–12 days for unripe).
- 🌡️ **Environmental Adjustment** — Shelf-life dynamically adjusted using **empirical formulas** derived from temperature, humidity, and gas readings (e.g., ammonia, ethanol).
- ⚙️ **Flask-based API** — Lightweight backend for:
  - Image upload and processing
  - Model inference
  - Integration-ready endpoints for IoT sensor nodes
- 🔬 **Research-based Implementation** — Designed for integration with multi-sensor grocery tracking systems

---

## 🧠 Machine Learning Model

- **Architecture:** Fine-tuned **MobileNetV2**
- **Dataset:** 13,478 labeled banana images across 4 ripeness stages
- **Frameworks:** TensorFlow, Keras
- **Performance:**
  - Accuracy: **98%**
  - Precision: **98%**
  - Recall: **98%**
  - F1-score: **98%**

---

## 🔧 Tech Stack

| Component               | Technology                       |
| ----------------------- | -------------------------------- |
| **Language**            | Python                           |
| **Backend**             | Flask                            |
| **Modeling**            | TensorFlow, Keras                |
| **Data Handling**       | NumPy, Pandas                    |
| **Environment Sensors** | DHT22, MQ135                     |
| **APIs**                | REST (Flask)                     |
| **Deployment**          | Local / Cloud-ready Flask server |

---

## 🧾 License

This project is licensed under the MIT License

---

## 🌟 Acknowledgments

TensorFlow & Keras for deep learning framework

Banana ripeness classification dataset (Kaggle)

Flask for lightweight API deployment
