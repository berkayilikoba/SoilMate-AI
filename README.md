# SoilMate AI
### AI-Powered Smart Soil Analysis & Regional Plant Care Management System

[cite_start]**SoilMate AI** is an advanced agricultural forecasting and risk management ecosystem built on **Huawei Cloud** and the **MindSpore** framework[cite: 15, 25]. [cite_start]Optimized for the 7 geographical regions of Turkey, the project combines deep learning models with cloud-based IoT data to generate strategic decisions for sustainable agriculture[cite: 25, 103].

---

## Achievements
* [cite_start]**Huawei Developer Competition:** First Place in Europe (Winner)[cite: 1].
* [cite_start]**Technology Partner:** Developed as part of the **Huawei Cloud & MindSpore** Ecosystem[cite: 15, 25].

---

## System Architecture

The project features an end-to-end cloud infrastructure designed to manage agricultural diversity and varying climatic conditions across different regions:

![SoilMate System Architecture](assets/architecture.png)

* [cite_start]**Edge Layer (Tarla):** In-field data is modeled using a Python Simulation (Sensor_Adana_01) which generates real-time sensor data (N, P, K, pH, and Moisture)[cite: 72, 88].
* [cite_start]**Cloud Ingestion:** Data is uploaded via MQTT to the **Huawei Cloud IoTDA** platform, which acts as the secure gateway for ingestion[cite: 72, 74].
* [cite_start]**Application Logic (Huawei ECS):** The core compute engine hosts the application logic and the interactive web dashboard[cite: 72, 77].
* [cite_start]**Data Storage & Model Registry (Huawei OBS):** **OBS** serves as the central hub for regional model weights and historical datasets[cite: 72, 76].
* [cite_start]**AI Services (Huawei ModelArts):** Historical data is processed by **ModelArts** using **MindSpore** to train predictive risk models[cite: 25, 75].
* [cite_start]**User Layer:** All insights and recommendations are presented through a **Streamlit** dashboard hosted on ECS[cite: 27, 72].

---

## AI Model & Data Flow

SoilMate AI utilizes a hybrid model structure to process diverse inputs and produce actionable agricultural prescriptions:

![SoilMate AI Model and Data Flow](assets/dataflow.png)

* [cite_start]**HybridModelGen:** A Bi-Directional LSTM architecture (64 units) that predicts Temperature, Rainfall, and Humidity[cite: 83].
* [cite_start]**HybridModelNDVI:** An LSTM-based model (16 units) focused on monitoring vegetation health via NDVI indices[cite: 84].
* [cite_start]**Key Outputs:** * **Crop Recommendation:** Precise suggestions for 1-month and 3-month periods[cite: 85].
    * [cite_start]**Risk Scoring:** Quantitative assessment of agricultural risks like drought or frost[cite: 85, 90].
    * [cite_start]**Actionable Suggestions:** Data-driven prescriptions to optimize resource use[cite: 71, 85].

---

## Key Features
* [cite_start]**Geographical Segmentation:** 7 distinct model architectures tailored to regional micro-climates in Turkey[cite: 103].
* [cite_start]**NDVI-Based Analysis:** AI-driven monitoring of plant health and vegetation indices[cite: 17, 26].
* [cite_start]**Long-Term Forecasting:** Accurate projections for 1-month and 3-month periods[cite: 26, 85].
* [cite_start]**Dynamic Risk Management:** Real-time reporting of environmental risks[cite: 85, 90].
* [cite_start]**Cost-Effective AI:** Models are trained in ModelArts but stored in OBS to avoid expensive always-on inference costs[cite: 92, 93].

---

## Demo Video
You can watch the project overview and system demonstration video here:
[Link to your Video - e.g., YouTube or Drive Link]

---

## Huawei Cloud Services Utilized

| Service | Function |
| :--- | :--- |
| **MindSpore** | [cite_start]Development and optimization of Gen & NDVI deep learning models [cite: 15, 25] |
| **ModelArts** | [cite_start]Distributed model training and AI lifecycle management [cite: 15, 75] |
| **OBS** | [cite_start]Secure storage for regional model weights and historical big data [cite: 15, 76] |
| **ECS** | [cite_start]Hosting the application logic and Streamlit-based analytical dashboard [cite: 15, 77] |
| **IoT DA** | [cite_start]Real-time ingestion and management of in-field sensor data [cite: 15, 74] |

---

[cite_start]**Developers:** Nisa GÜVELOĞLU, Akın KAFADAR, Berkay ILIKOBA, Münevver DEMİRAY [cite: 57, 58, 59, 60]
