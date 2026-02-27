# Soilmate AI 
### AI-Powered Smart Soil Analysis & Regional Plant Care Management System

**Soilmate AI** is an advanced agricultural forecasting and risk management ecosystem built on **Huawei Cloud** and the **MindSpore** framework. Optimized for the 7 geographical regions of Turkey, the project combines deep learning models with cloud-based IoT data to generate strategic decisions for sustainable agriculture.

---

## Achievements
* **Huawei Developer Competition:** 🥇 **First Place in Europe (Winner)**
* **Technology Partner:** Developed as part of the **Huawei Cloud & MindSpore** Ecosystem.

---

## Technical Architecture & Workflow

The project features an end-to-end pipeline designed to manage agricultural diversity and varying climatic conditions across different regions:

* **Regional Model Training (ModelArts & MindSpore):** Turkey is segmented into 7 distinct geographical regions. Independent **Genetic and NDVI models** have been trained using region-specific datasets to account for micro-climates.
* **Model Storage & Management (OBS):** Specialized model weights for each region are categorized and stored on **Huawei OBS (Object Storage Service)** for high availability and seamless retrieval.
* **Data Processing & IoT:** Real-time environmental data (Temperature, Humidity, Rainfall) is ingested from field sensors through the **Huawei Cloud IoT DA** platform.
* **Intelligent Forecasting:** Utilizing historical data and NDVI analysis, the system generates high-precision forecasts for temperature, humidity, and rainfall on **1-month and 3-month** scales.
* **Risk Scoring & Recommendation Engine:** Forecast results are converted into dynamic, region-specific risk scores, providing users with actionable agricultural advice.
* **Visualization (ECS & Streamlit):** This entire architecture is visualized through an interactive **Streamlit** dashboard hosted on a **Huawei ECS (Elastic Cloud Server)** instance.

---

## Key Features

* 📍 **Geographical Segmentation:** 7 distinct model architectures tailored to regional micro-climates.
* 📊 **NDVI-Based Analysis:** AI-driven monitoring of plant health and vegetation indices.
* 🔮 **Long-Term Forecasting:** Accurate climate projections for 1-month and 3-month periods.
* ⚠️ **Dynamic Risk Management:** Real-time reporting of risks such as drought, frost, or excessive rainfall.
* 💡 **Smart Recommendations:** Strategic planting and maintenance advice based on predictive analytics.

---

## Huawei Cloud Services Utilized

| Service | Function |
| :--- | :--- |
| **MindSpore** | Development and optimization of Gen & NDVI deep learning models |
| **ModelArts** | Distributed model training and AI lifecycle management |
| **OBS** | Secure storage of regional model weights and large datasets |
| **ECS** | 24/7 hosting of the Streamlit-based analytical dashboard |
| **IoT DA** | Real-time data ingestion from field sensors |

---

**Developers:** Nisa GÜVELOĞLU, Akın KAFADAR, Berkay ILIKOBA 
