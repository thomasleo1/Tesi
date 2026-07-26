# Smart Hazard Notification System for Outdoor Workplaces

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Android](https://img.shields.io/badge/Platform-Wear%20OS-green.svg)](https://developer.android.com/wear)

This project was developed as a Bachelor's Degree Thesis in **Computer Networks** at the **University of Salento** (A.Y. 2023-2024).  
The primary goal is to develop an **Internet of Things (IoT)** system aimed at collision prevention and increasing operator safety in outdoor work environments involving remotely controlled vehicles or heavy construction machinery.

## 📸 Screenshots & Preview

<table>
  <tr>
    <td align="center" width="30%">
      <b>Wear OS App</b><br/><br/>
      <img src="https://github.com/user-attachments/assets/3df40c05-1850-4639-a59f-6bbe1e848770" width="100%" alt="Wear OS App" />
    </td>
    <td align="center" width="70%">
      <b>Server Dashboard</b><br/><br/>
      <img src="https://github.com/user-attachments/assets/1b493784-47ab-46e4-8291-7b92585fb39a" width="100%" alt="Server Dashboard" />
    </td>
  </tr>
</table>

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

## 🚀 Installation & Setup Guide

### 1. Web Server Configuration

Navigate to the server directory and install the required dependencies:

```bash
pip install flask flask-sqlalchemy
```

Start the web server:

```bash
python server.py
```

> **Note:** By default, the server listens on port `5000`.

---

### 2. Wear OS App Setup

1. Open the `Wear Os` folder in **Android Studio**.
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
   sudo python client.py
   ```

---

## 👨‍💻 Author

* **Thomas Leo**
  * **GitHub:** [@thomasleo1](https://github.com/thomasleo1)
  * **Academic Email:** [thomas.leo@studenti.unisalento.it](mailto:thomas.leo@studenti.unisalento.it)
  * **Personal Email:** [thomasleo2704@gmail.com](mailto:thomasleo2704@gmail.com)
  * **University:** Università del Salento
  * **Degree Program:** Information Engineering (*Ingegneria dell'Informazione*)
  * **Course:** Software Engineering Principles (*Principi di Ingegneria del Software*)
