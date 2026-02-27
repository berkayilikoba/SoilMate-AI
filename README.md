# SoilMate AI

### AI-Powered Smart Soil Analysis & Regional Plant Care Management System

**SoilMate AI** is an end-to-end Smart Agriculture SaaS solution designed to combat inefficient resource usage and yield loss in farming. Built on **Huawei Cloud** and the **MindSpore** framework, the system replaces traditional guesswork with data-driven precision, specifically optimized for the 7 geographical regions of Turkey.

---

## Achievements

* **Huawei Developer Competition:** First Place in Europe (Winner)
* **Technology Partner:** Developed as part of the Huawei Cloud & MindSpore Ecosystem

---

## Technical Architecture & Workflow

The project features a robust cloud infrastructure designed to manage agricultural diversity and varying climatic conditions.

### System Layers

#### Edge Layer (Field)

In-field data is modeled using a Python simulation (`Sensor_Adana_01`) which generates real-time sensor data including:

* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)
* pH
* Moisture

#### Cloud Ingestion

Data is uploaded via MQTT to **Huawei Cloud IoTDA**, acting as the secure gateway for ingestion and device management.

#### Application Logic (Huawei ECS)

The core compute engine hosts the backend logic and interactive web dashboard, ensuring 24/7 availability.

#### Data Storage & Model Registry (Huawei OBS)

OBS stores:

* Regional model weights
* Historical datasets (CSV)
* AI artifacts

#### AI Services (Huawei ModelArts)

Historical data is processed in ModelArts to train predictive risk models using MindSpore. Trained models are stored back in OBS.

---

## AI Model & Data Flow

SoilMate AI utilizes a hybrid model structure to process diverse inputs and produce actionable insights.

### Models

* **HybridModelGen:** Bi-Directional LSTM (64 units) predicts Temperature (T), Rainfall (R), and Humidity (H).
* **HybridModelNDVI:** LSTM-based model (16 units) monitors vegetation health using NDVI indices.

---

## Cloud Security & Compliance (Defense in Depth)

Security is a core pillar of SoilMate AI. We implemented a strict **"Defense in Depth"** strategy to ensure data integrity and system availability:

* **VPC & Strict Security Groups:** Our `SoilMate-SG` network rules are strictly configured. We only expose **Port 8501** for the Streamlit dashboard and **Port 22** for secure admin access. All other ports are completely blocked.
* **Identity and Access Management (IAM):** We strictly follow the **Principle of Least Privilege**. The root account is never used for daily operations. Instead, dedicated IAM users and temporary **AK/SK (Access Key/Secret Key)** credentials are used for API communications (e.g., writing to OBS).
* **Host Security Service (HSS):** Our ECS server is actively monitored by **Huawei HSS** from the inside, scanning for vulnerabilities and automatically blocking malicious activities like Brute Force attacks. The server is officially certified as **"Protected"** by Huawei Cloud.

---

## Observability & Autonomous Monitoring

To guarantee 24/7 uninterrupted service for farmers, we implemented proactive monitoring:

* **Huawei Cloud Eye:** Continuously monitors the health of our ECS compute engine.
* **Autonomous Alarms:** We configured a custom alarm rule: If the server's CPU usage exceeds **80%**, the system automatically triggers an alert via **Mail/SMS**. This allows us to catch and resolve potential bottlenecks before the server crashes.

---

## Key Features

* **Geographical Segmentation:** 7 distinct model architectures tailored to regional micro-climates.
* **NDVI-Based Analysis:** AI-driven monitoring of vegetation health.
* **Long-Term Forecasting:** 1-month and 3-month predictive projections.
* **Dynamic Risk Management:** Real-time environmental risk reporting.
* **Cost-Effective AI Infrastructure:** Models trained in ModelArts and stored in OBS to avoid always-on inference costs.

---

## Demo & Live Dashboard

* **Demo Site:** [http://188.239.52.182:8501/](http://188.239.52.182:8501/)
* **Demo Video:** [[link](https://youtu.be/XHE3Vss5oUo)]

---

## Huawei Cloud Services Used

| Service | Purpose |
| --- | --- |
| **MindSpore** | Deep learning model development & optimization |
| **ModelArts** | Distributed training & AI lifecycle management |
| **OBS** | Secure storage for model weights & datasets |
| **ECS** | Backend logic & Streamlit dashboard hosting |
| **IoTDA** | Real-time sensor data ingestion & device management |
| **HSS** | Host Security & Vulnerability Scanning |
| **Cloud Eye** | Real-time Performance Monitoring & Alarms |
| **IAM** | Identity Management & Resource Access Control |

---

## Team Cukurova

* **Nisa GÜVELOĞLU** — Team Leader & IoT Integration
* **Akın KAFADAR** — Cloud Architect
* **Berkay ILIKOBA** — AI Architect

---

Başka bir ekleme yapmak istersen buradayım Berkay. GitHub profiline bu halini eklememi ister misin?
