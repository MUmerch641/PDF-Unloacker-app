# PDF Unlocker Mobile Application

A minimal, professional React Native mobile application to unlock password-protected PDFs automatically.

## Project Overview

This application allows users to upload locked PDF files, removes their security restrictions (both Owner and User passwords) using a robust backend service, and provides an unlocked version for download or in-app viewing.

## Features

- **📂 PDF Upload**: Select locked PDFs from device storage with file details.
- **🔓 Smart Unlock**:
  - Automatically removes "Owner Restrictions" (print/copy blocks) instantly.
  - Cracks "User Passwords" (open blocks) using a Dictionary Attack + Numeric Brute Force engine.
- **👁️ In-App Viewer**: Preview unlocked PDFs directly within the app without leaving.
- **💾 Download**: Save unlocked files to your device.
- **clean UI**: Professional, centered, and responsive design.

## Technical Stack

- **Frontend**: React Native (Expo), `react-native-webview`, `axios`, `expo-document-picker`.
- **Backend**: Python (FastAPI), `pikepdf`, `qpdf`.
- **Security**: Auto-deletion of files immediately after processing.

---

## Setup & Installation

### Prerequisites
- Node.js & npm
- Python 3.8+
- Expo Go app on your mobile device (Android/iOS)

### 1. Backend Setup (Python)

The backend handles the CPU-intensive password removal.

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    *Note: The server must run on `0.0.0.0` to be accessible from your mobile device.*

### 2. Frontend Setup (React Native)

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  **Configure API URL**:
    - Open `App.js`.
    - Find the `LAN_IP` constant at the top.
    - Update it to your computer's local LAN IP address (e.g., `192.168.1.5`).
    - *You can find this by running `ifconfig` (Mac/Linux) or `ipconfig` (Windows).*

4.  Start the app:
    ```bash
    npx expo start
    ```
5.  Scan the QR code with the **Expo Go** app on your phone.

---

## Building the Test APK (Android)

To generate a standalone `.apk` file for Android testing:

1.  Install EAS CLI:
    ```bash
    npm install -g eas-cli
    ```
2.  Login to your Expo account:
    ```bash
    eas login
    ```
3.  Configure the build:
    ```bash
    eas build:configure
    ```
4.  Run the build command:
    ```bash
    eas build -p android --profile preview
    ```
    *This will generate a downloadable APK link after the build completes in the cloud.*

---

## Troubleshooting

- **"Network request failed"**: Ensure your phone and computer are on the **same WiFi network** and you updated `LAN_IP` in `App.js`.
- **"Password not found"**: The app tries the top 50,000 common passwords and all 4-digit PINs. If the password is extremely complex and random, it cannot be cracked by software alone.
# PDF-Unloacker-app
