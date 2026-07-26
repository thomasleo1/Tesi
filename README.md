# Smart Hazard Notification System for Outdoor Workplaces

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Android](https://img.shields.io/badge/Platform-Wear%20OS-green.svg)](https://developer.android.com/wear)

This project was developed as a Bachelor's Degree Thesis in **Computer Networks** at the **University of Salento** (A.Y. 2023-2024).  
The primary goal is to develop an **Internet of Things (IoT)** system aimed at collision prevention and increasing operator safety in outdoor work environments involving remotely controlled vehicles or heavy construction machinery.

---

## 📌 System Architecture

The overall system is divided into three main modules that communicate with each other:

1. **Raspberry Pi 4 (Vehicle Unit):**
   * **BLE Scanning:** Continuously scans the surrounding area for operators/obstacles wearing Bluetooth Beacons using the integrated Bluetooth module (`bluepy`).
   * **Distance Estimation:** Estimates distance based on RSSI values received from the beacons.
   * **Push Notification Dispatch:** Sends real-time alerts to the operator's smartwatch via a second Bluetooth adapter (USB Dongle) and the RFCOMM protocol (`PyBluez`).
   * **Data Forwarding:** Transmits detection data (MAC address, distance, danger/warning status) to a centralized server via HTTP POST.

2. **Wear OS Smartwatch (Wearable Device):**
   * Android application developed in **Java** running as a background service (`BluetoothService`).
   * Receives alert messages from the Raspberry Pi via Bluetooth RFCOMM and displays them to the operator as notifications with audio/haptic alerts.

3. **Centralized Web Server (Flask + SQLite/SQLAlchemy):**
   * Receives data sent by the Raspberry Pi and stores it in a database.
   * Provides an authentication-protected web interface (Login) to review event logs and detection statuses (e.g., *Warning* or *Danger*).

---

## 🛠️ Technologies and Hardware Used

### Hardware
* **Raspberry Pi 4**
* **USB Bluetooth Dongle** (for additional interface)
* **Huawei LEO-BX9 Smartwatch** (Wear OS, Bluetooth 4.1)
* **BLE Bluetooth Beacons** (e.g., BlueUp)

### Software & Libraries
* **Python 3**
  * `bluepy` (BLE Scanning)
  * `pybluez` (RFCOMM / Standard Bluetooth Communication)
  * `Flask` & `Flask-SQLAlchemy` (Web Server & Database)
  * `requests` (HTTP POST requests)
* **Java / Android SDK** (Wear OS app development)

---

## 📁 Repository Structure

```text
├── raspberry/
│   └── scan_and_notify.py    # Python script for BLE scanning, distance estimation, and alert/data transmission
├── server/
│   ├── app.py                # Flask Web Server and SQLAlchemy Database management
│   └── templates/            # HTML Templates (login.html, data.html)
└── wear_os_app/              # Android Studio Project for the smartwatch
    ├── app/src/main/java/    # Java source code (MainActivity, BluetoothService)
    └── AndroidManifest.xml   # Bluetooth permissions and service configuration
```

---

## 🚀 Installation & Setup Guide

### 1. Web Server Configuration

Navigate to the server directory and install the required dependencies:

```bash
pip install flask flask-sqlalchemy
```

Start the web server:

```bash
python app.py
```

> **Note:** By default, the server listens on port `5000`.

---

### 2. Wear OS App Setup

1. Open the `wear_os_app` folder in **Android Studio**.
2. Verify that `AndroidManifest.xml` includes the necessary Bluetooth permissions:
   - `BLUETOOTH_CONNECT`
   - `BLUETOOTH_SCAN`
   - `POST_NOTIFICATIONS`
3. Build and install the APK onto the smartwatch using **ADB** or **Wi-Fi Debugging**.

---

### 3. Running the Script on Raspberry Pi

1. Ensure the USB Bluetooth Dongle is plugged in and recognized:
   ```bash
   hciconfig
   ```
2. Install the required Python libraries:
   ```bash
   pip install bluepy pybluez requests
   ```
3. Configure the target MAC addresses inside the Python script:
   - USB Dongle Bluetooth interface
   - Smartwatch MAC address
   - Web Server IP address
4. Run the script with root privileges (required for direct access to Bluetooth sockets):
   ```bash
   sudo python scan_and_notify.py
   ```

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Thomas Leo** - Undergraduate in Information Engineering (*University of Salento*)  
**Advisor:** Prof. Luigi Patrono

---

### 💡 Additional Recommendations to Improve the Repository:
1. **File Reorganization:** Keep file and folder names consistent with the structure defined in `README.md`.
2. **`.gitignore` File:** Add a `.gitignore` file to prevent committing temporary files or build directories (`__pycache__/`, `.idea/`, `.gradle/`, `build/`, etc.).

### 💡 Consigli aggiuntivi per migliorare la repository:
1. **Riorganizzazione dei file:** Se la cartella contiene codice sorgente (es. script Python, progetto Android Studio, ecc.), assegna loro nomi coerenti con la struttura descritta nel `README.md`.
2. **File `.gitignore`:** Aggiungi un file `.gitignore` per evitare di caricare file temporanei o cartelle di build (`__pycache__/`, `.idea/`, `.gradle/`, ecc.).            # Progetto Android Studio per lo smartwatch
    ├── app/src/main/java/    # Codice sorgente Java (MainActivity, BluetoothService)
    └── AndroidManifest.xml   # Permessi Bluetooth e configurazione servizi
