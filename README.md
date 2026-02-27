# Soilmate AI 
### AI-Powered Smart Soil Analysis & Regional Plant Care Management System

**Soilmate AI** is an advanced agricultural forecasting and risk management ecosystem built on **Huawei Cloud** and the **MindSpore** framework. Specifically optimized for the 7 geographical regions of Turkey, the project combines deep learning models with cloud-based IoT data to generate strategic decisions for sustainable agriculture.

This platform allows farmers and agricultural planners to make data-driven decisions by providing region-specific forecasts and risk assessments, ultimately aiming for increased yield and environmental sustainability.

---

## Achievements
* **Huawei Developer Competition:** First Place in Europe (Winner)
* **Technology Partner:** Developed as part of the **Huawei Cloud & MindSpore** Ecosystem.

---

## System Architecture

The project is built on a robust, end-to-end cloud infrastructure that facilitates data flow from the field to a user-facing dashboard. The architecture is composed of an Edge Layer, a rich Huawei Cloud Platform Layer, and a User Layer.

![Soilmate AI System Architecture Diagram](path/to/your/image_1.png)

### Architectural Workflow

1.  **Edge Layer (Tarla):** In-field data is currently modeled using a **Python Simulation (Sensor\_Adana\_01)** which generates sensor data for the selected region.
2.  **Cloud Ingestion:** This simulation uploads data via **MQTT Data Upload** to the **Huawei Cloud IoTDA** platform (the Ingestion & MQTT Gateway).
3.  **Application Logic (Huawei ECS):** From IoTDA, data is forwarded to the **Huawei ECS (App Server)**.
    * The App Server requests models from storage.
    * It processes incoming sensor data alongside returned models.
    * It generates results for **Prediction**, **Risk Analysis**, and **Recommendation**.
    * It simultaneously archives sensor data in storage.
4.  **Data Storage & Model Registry (Huawei OBS):** **OBS** serves as the central storage hub, managing:
    * Regional model weights (Trained Models).
    * Historical sensor data.
5.  **AI Services (Huawei ModelArts):** Historical data is sent from OBS to **ModelArts** for continuous or one-time **AI Prediction**, and the resulting Trained Models are sent back to OBS.
6.  **User Layer:** All processed information and recommendations are streamed to an interactive **Smart Dashboard (Streamlit)** for user access.

---

## AI Model & Data Flow

At the heart of Soilmate AI is a core logic that processes diverse input data through specialized models to produce actionable insights.

![Soilmate AI AI Model and Data Flow Diagram](https://github.com/user-attachments/assets/689edcab-769a-414f-87bc-21b9f620b87c)

### Inputs, Models, and Outputs

* **Data Inputs:**
    * **IoT Device:** Provides direct in-field data: **N**itrogen, **P**hosphorus, **K**assium, and **pH**.
    * **HybridModelGen:** A data simulation component that generates regional weather-related parameters: **T**emperature (T), **R**ainfall (R), **H**umidity (H), **E**vapotranspiration (ET), and **S**oil **M**oisture (SM).
    * **HybridModelNDVI:** Focuses on vegetation health, providing Normalized Difference Vegetation Index (**NDVI**) data.
* **Specialized AI Models:**
    * **Crop Recommendation Model:** Processes Nitrogen, Potassium, pH (from IoT) and Temperature, Rainfall, Humidity (from HybridModelGen).
    * **Risk Analysis and Suggestion Model:** Processes Temperature, Rainfall, Humidity, Evapotranspiration, Soil Moisture (from HybridModelGen) and NDVI (from HybridModelNDVI).
* **AI-Generated Outputs:**
    * **Crop Recommendation (1 month):** Immediate agricultural suggestions.
    * **Crop Recommendation (3 months):** Longer-term agricultural planning advice.
    * **Risk Score:** Quantitative assessment of agricultural risks.
    * **Suggestion:** Categorical actions based on risk and analysis.

---

## Key Features

* **Geographical Segmentation:** 7 distinct model architectures tailored to regional micro-climates of Turkey.
* **NDVI-Based Analysis:** AI-driven monitoring of plant health and vegetation indices.
* **Long-Term Forecasting:** Accurate climate and crop projections for 1-month and 3-month periods.
* **Dynamic Risk Management:** Real-time reporting and scoring of risks such as drought or excessive rainfall.
* **Smart Recommendations:** Strategic crop selection and maintenance advice based on predictive analytics.

---

## Demo Video

You can watch the project overview and system demonstration video here:
[[Link](https://youtu.be/XHE3Vss5oUo)]

---

## Huawei Cloud Services Utilized

| Service | Function |
| :--- | :--- |
| **MindSpore** | Primary deep learning framework for Gen & NDVI model development and optimization |
| **ModelArts** | Distributed model training, AI lifecycle management, and prediction services |
| **OBS (Object Storage)** | Secure and centralized storage for regional model weights and data archives |
| **ECS (Elastic Cloud)** | 24/7 hosting for the Streamlit-based dashboard and core application logic |
| **IoT DA** | Real-time ingestion and management of in-field sensor data |

---

**Developers:** Nisa GÜVELOĞLU, Akın KAFADAR, Berkay ILIKOBA
