# Industrial Equipment Monitoring System with Predictive Maintenance

## Overview

This project implements a cloud-based Industrial IoT (IIoT) system to monitor equipment health in real time using Azure services. The system simulates sensor data, processes it for anomalies, stores it for historical analysis, and uses a machine learning model to predict equipment failures before they occur. Alerts are triggered through Logic Apps for immediate user notification.

---

## System Architecture

The system consists of the following components:

1. **Simulated IoT Device**: Sends sensor data to Azure.
2. **Azure IoT Hub**: Ingests telemetry data.
3. **Azure Stream Analytics**: Processes real-time data and routes it.
4. **Azure Blob Storage**: Stores telemetry logs for analysis.
5. **Azure Machine Learning**: Predicts failures based on sensor patterns.
6. **Azure Logic Apps**: Sends real-time alerts for critical events.

---

## 1. Sensor Data Simulation

### Functionality

- Simulates a Raspberry Pi sending:
  - `temperature (°C)`
  - `vibration (g)`
  - `power_usage (Watts)`
  - `timestamp`
- Data is transmitted every 5 seconds.

### Implementation

- Python script using the Azure IoT Device SDK.
- Data randomized within safe and failure-prone ranges.
- Sends telemetry to Azure IoT Hub via MQTT protocol.

---

## 2. Azure IoT Hub

### Purpose

- Entry point for all telemetry data.
- Manages device identity and communication.
- Integrates with downstream services like Stream Analytics.

### Setup

- IoT Hub created in the same resource group as other services.
- Registered device and obtained connection string for the simulator.

---

## 3. Azure Stream Analytics

### Purpose

- Real-time telemetry filtering, transformation, and routing.
- Detects anomaly thresholds and pushes alerts.

### Inputs & Outputs

- **Input**: IoT Hub
- **Output 1**: Azure Blob Storage (all data)
- **Output 2**: Azure Logic Apps (filtered data)
- **Output 3**: Azure ML Endpoint (for predictions)

### Query for Storage

```sql
SELECT
    System.Timestamp AS event_time,
    AVG(temperature) AS avg_temperature,
    AVG(vibration) AS avg_vibration,
    AVG(power_usage) AS avg_power_usage
INTO SensorOutput
FROM SensorInput
GROUP BY TumblingWindow(hour,1)
```

## 4. Azure Blob Storage

### Purpose

- Stores all telemetry logs from Stream Analytics.
- Data is written as JSON files and time-partitioned (e.g., by hour/day).

### Benefits

- Used as historical data for audits and analytics.
- Acts as the **primary dataset source** for training the ML model.
- Easy to access with tools like Azure Data Explorer or Azure ML.
- Lifecycle management enabled to **auto-delete older data** and reduce costs.

---

## 5. Azure Machine Learning (Implemented)

### Purpose

- Detect and predict **equipment failures** using historical sensor behavior.
- Provide **real-time predictions** from streaming sensor data.

### Implementation Steps

1. **Workspace**: Created `equipment-ml-workspace`.
2. **Dataset**: Imported logs from Blob Storage, labeled failure conditions as:
   - `temperature > 70°C`
   - `vibration > 8.0g`
3. **AutoML**: Trained a **binary classification model** to detect failures.
4. **Deployment**: Published the model as a **real-time REST endpoint**.
5. **Integration**: Connected the endpoint to **Stream Analytics** to score live data.

### Endpoint Behavior

- Receives real-time telemetry as input.
- Outputs a `failure_probability` between 0 and 1.
- If prediction exceeds **0.85**, it's treated as an imminent failure.
- Stream Analytics routes this to Logic Apps for real-time alerting.

---

## 6. Azure Logic Apps (Implemented)

### Purpose

- Send real-time **notifications via Email or SMS** when:
  - Sensor values cross critical thresholds.
  - Machine Learning predicts an imminent failure.

### Workflow

1. Triggered when Stream Analytics detects anomaly or receives high ML score.
2. Parses incoming JSON from telemetry.
3. Checks the following **conditions**:
   - `temperature > 70`
   - `vibration > 8.0`
   - `failure_probability > 0.85`
4. Sends out notifications via:
   - **Outlook 365 / Gmail** (Email)
   - **Twilio** (SMS)

### 🔹 Features

- No-code, scalable automation using Azure Logic App Designer.
- Each alert message includes:
  - Sensor data snapshot (temp, vib, power usage)
  - Timestamp
  - Prediction probability
- Can be extended to integrate with:
  - Microsoft Teams
  - Slack
  - PagerDuty
  - ServiceNow

---
