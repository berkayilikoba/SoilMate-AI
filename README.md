# SoilMate AI

### AI-Powered Smart Soil Analysis & Regional Plant Care Management System

**SoilMate AI** is an end-to-end Smart Agriculture SaaS solution designed to combat inefficient resource usage and yield loss in farming. Built on **Huawei Cloud** and the **MindSpore** framework, the system replaces traditional guesswork with data-driven precision, specifically optimized for the 7 geographical regions of Turkey.

---

## Achievements

* **Huawei Developer Competition:** 🥇 First Place in Europe (Winner)
* **Technology Partner:** Developed as part of the Huawei Cloud & MindSpore Ecosystem

---

## Technical Architecture & Workflow

![Technical Architecture](https://github.com/user-attachments/assets/0abc9ba8-cc17-4f84-a53f-cbd6abda374b)

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
![AI Model & Data Flow](https://github.com/user-attachments/assets/a6dcc3c8-98c6-40a5-960a-b9deb6adb18e)


SoilMate AI utilizes a hybrid model structure to process diverse inputs and produce actionable insights.

### Models

* **HybridModelGen:** Bi-Directional LSTM (64 units) predicts Temperature (T), Rainfall (R), and Humidity (H).
* **HybridModelNDVI:** LSTM-based model (16 units) monitors vegetation health using NDVI indices.

---
---

## Cloud Security & Compliance

SoilMate AI is built on a **Defense in Depth** security architecture to ensure data integrity, availability, and operational resilience.

* **VPC & Security Groups:** Minimal attack surface. Only **Port 8501** (Dashboard) and **Port 22** (SSH Admin) are exposed. All other ports are strictly blocked.
* **IAM & Least Privilege:** Root accounts are never used. Access is managed via dedicated IAM users and temporary **AK/SK** credentials for secure API communication.
* **Host Security (HSS):** Continuous vulnerability scanning, brute-force attack detection, and real-time protection. ECS instance status: **Protected**.

---

## Observability & Monitoring

Proactive infrastructure monitoring ensures uninterrupted 24/7 service.

* **Cloud Eye:** Real-time performance and health monitoring of the ECS compute engine.
* **Autonomous Alerts:** Automated Mail/SMS notifications triggered when CPU usage exceeds **80%**, enabling preventive incident response.

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
