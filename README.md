```markdown
# SoilMate AI - Agricultural Decision Support System 🌾🤖

[![Huawei Developer Competition 2025 Europe Winner](https://img.shields.io/badge/Huawei%20Developer%20Competition-First%20Place%20(Europe)-gold)](https://huawei.com)
[![Python 3.13](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![TensorFlow / Keras](https://img.shields.io/badge/TensorFlow-Keras-orange.svg)](https://tensorflow.org/)
[![Google Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-API-green.svg)](https://earthengine.google.com/)

SoilMate AI is a hybrid artificial intelligence architecture that optimizes agricultural processes and provides long-term projections by harmonizing climate data, satellite vegetation indices (MODIS, Sentinel-2), and soil characteristics. It achieved **First Place in Europe** at the Huawei Developer Competition 2025.

---

## 🚀 Project Architecture & Features

- **Data Acquisition (Google Earth Engine):** Automated extraction of ERA5-Land daily climate/soil moisture, MODIS (NDVI, EVI, LST), and Sentinel-2 (NDWI) datasets in 4-year chunks between 2000 and 2026.
- **Flexible Time-Series Resampling:** Resampling daily data into 3, 5, 7, 10, 14, 15, 20, and 30-day (monthly) periods with optimized cumulative variables.
- **HybridModelGen Architecture:** A specialized deep learning structure composed of **Bi-Directional LSTM (64 units) -> Dropout (20%) -> Unidirectional LSTM (32 units) -> Dense layers** designed to capture complex temporal patterns.

---

## 📁 Project Structure

```text
SoilMate2/
│
├── Master Data/             # Raw and merged master CSVs extracted via GEE
├── Sample Data/             # Grouped datasets for 3, 5, 7, 10, 14, 15, 20, and 30-day periods
├── models/                  # Trained LSTM weights and model checkpoints
├── notebooks/               # Colab and Jupyter analysis notebooks
└── README.md

```

---

## ⚙️ Installation & Usage

1. **Clone the Repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/SoilMate2.git](https://github.com/YOUR_USERNAME/SoilMate2.git)
cd SoilMate2

```


2. **Run via Google Colab:**
* Upload your project files to your Google Drive under `/MyDrive/SoilMate2/Sample Data/`.
* Open the respective notebooks, authenticate with Google Earth Engine (`ee.Authenticate()`), and execute the model training cells.



---

## 📊 Performance & Metrics

The system is evaluated on dynamic metrics such as temperature, vegetation indices (NDVI/EVI), and soil moisture using $R^2$ (R-Squared), MSE, and MAE metrics, automatically determining the optimal grouping periods for each agricultural parameter.

---

## 🏆 License & Copyright

This project belongs to the **SoilMate AI** development team. All rights reserved; protected as a private repository.

```

```
