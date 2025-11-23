# Setup Guide - Gramin GPT Starter

Follow these steps to get the starter running locally or on Replit.

## 1. Firebase
1. Create a Firebase project: https://console.firebase.google.com
2. Add a Web App and copy the firebaseConfig object (apiKey, authDomain, projectId, storageBucket, messagingSenderId, appId).
3. Enable **Phone** authentication (Authentication → Sign-in method).
4. Create a **Service Account** (Project Settings → Service Accounts → Generate Private Key) and save the JSON file.
   - Keep the file safe and DO NOT commit it.
5. Create a Firestore database (Native mode).
6. Enable Firebase Storage.

## 2. OpenAI
1. Get an API key from https://platform.openai.com
2. Keep it ready for backend use.

OpenAI API key: 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

## 3. Backend (FastAPI)
- Requirements: Python 3.10+, pip
- Create a `.env` in `backend/` (copy from `.env.example`) and fill the variables:
  - OPENAI_API_KEY
  - FIREBASE_SERVICE_ACCOUNT (path to service account JSON on the server; optional for prototype)
  - FIREBASE_STORAGE_BUCKET (e.g., your-project-id.appspot.com)
- Install dependencies:
  ```
  cd backend
  pip install -r requirements.txt
  ```
- Run locally:
  ```
  uvicorn main:app --host 0.0.0.0 --port 8000
  ```

## 4. Frontend (React PWA)
- Requirements: Node 18+, npm
- In `frontend/`, copy `.env.example` to `.env` and set `REACT_APP_BACKEND_URL` to your backend URL.
- Install and run:
  ```
  cd frontend
  npm install
  npm start
  ```

