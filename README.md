# SoilMate AI  
### AI-Powered Smart Soil Analysis & Regional Plant Care Management System

**SoilMate AI** is an end-to-end Smart Agriculture SaaS solution designed to combat inefficient resource usage and yield loss in farming. Built on **Huawei Cloud** and the **MindSpore** framework, the system replaces traditional guesswork with data-driven precision, specifically optimized for the 7 geographical regions of Turkey.

---

## Achievements

- **Huawei Developer Competition:** First Place in Europe (Winner)  
- **Technology Partner:** Developed as part of the Huawei Cloud & MindSpore Ecosystem  

---

## Technical Architecture & Workflow

The project features a robust cloud infrastructure designed to manage agricultural diversity and varying climatic conditions.

![System Architecture](https://github.com/user-attachments/assets/82d410e1-edc0-442c-89ce-a97b431532ac)

### System Layers

### Edge Layer (Field)
In-field data is modeled using a Python simulation (`Sensor_Adana_01`) which generates real-time sensor data including:

- Nitrogen (N)  
- Phosphorus (P)  
- Potassium (K)  
- pH  
- Moisture  

---

### Cloud Ingestion
Data is uploaded via MQTT to **Huawei Cloud IoTDA**, acting as the secure gateway for ingestion and device management.

---

### Application Logic (Huawei ECS)
The core compute engine hosts the backend logic and interactive web dashboard, ensuring 24/7 availability.

---

### Data Storage & Model Registry (Huawei OBS)
OBS stores:

- Regional model weights  
- Historical datasets (CSV)  
- AI artifacts  

---

### AI Services (Huawei ModelArts)
Historical data is processed in ModelArts to train predictive risk models using MindSpore. Trained models are stored back in OBS.

---

## AI Model & Data Flow

SoilMate AI utilizes a hybrid model structure to process diverse inputs and produce actionable insights.

![AI Model and Data Flow](https://github.com/user-attachments/assets/dd24019f-e031-4774-9824-82e7a480acc8)

### Models

#### HybridModelGen
- Bi-Directional LSTM (64 units)  
- Predicts:
  - Temperature (T)  
  - Rainfall (R)  
  - Humidity (H)

#### HybridModelNDVI
- LSTM-based model (16 units)  
- Monitors vegetation health using NDVI indices  

---

## Key Outputs

- **Crop Recommendation**  
  Precise suggestions for 1-month and 3-month planning  

- **Risk Scoring**  
  Quantitative assessment of agricultural risks such as drought or frost  

- **Actionable Suggestions**  
  Data-driven prescriptions for optimized fertilizer and water usage  

---

## Key Features

- **Geographical Segmentation**  
  7 distinct model architectures tailored to regional micro-climates  

- **NDVI-Based Analysis**  
  AI-driven monitoring of vegetation health  

- **Long-Term Forecasting**  
  1-month and 3-month predictive projections  

- **Dynamic Risk Management**  
  Real-time environmental risk reporting  

- **Cost-Effective AI Infrastructure**  
  Models trained in ModelArts and stored in OBS to avoid always-on inference costs  

---

## Demo & Live Dashboard

- **Demo Site:**  
  http://188.239.52.182:8501/

- **Demo Video:**  
  [Add your video link here]

---

## Huawei Cloud Services Used

| Service | Purpose |
|----------|----------|
| **MindSpore** | Deep learning model development & optimization |
| **ModelArts** | Distributed training & AI lifecycle management |
| **OBS** | Secure storage for model weights & datasets |
| **ECS** | Backend logic & Streamlit dashboard hosting |
| **IoTDA** | Real-time sensor data ingestion & device management |

---

## Team Cukurova

- **Nisa GÜVELOĞLU** — IoT Integration
- **Akın KAFADAR** — Cloud Architect
- **Berkay ILIKOBA** — AI Architect

---
