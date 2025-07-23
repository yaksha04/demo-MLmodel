A modular ML model that uses **Streamlit** for the frontend and **FastAPI** for the backend. The system tracks machine learning model versions stored in a structured directory, and automatically detects changes based on hash tracking to notify the frontend.

---

## 📁 Project Structure

```

MLmodel-demo/
├── apple/
│   ├── 0001/
│   │   ├── L1/id.txt
│   │   └── L2/id.txt
├── mango/
│   ├── 0002/
│   │   ├── L1/id.txt
│   │   └── L2/id.txt
├── tec/
│   ├── 0003/
│   │   ├── L1/id.txt
│   │   └── L2/id.txt
├── backend/
│   └── main.py        # FastAPI app
├── frontend/
│   └── app.py         # Streamlit app
└── README.md

````

---

## 🚀 Features

- 📦 Organized versioned model structure (`apple`, `mango`, etc`)
- 🔒 Hash-based file change detection using `id.txt` in each L1/L2
- 🔔 Backend tracks file changes and notifies frontend
- ⚡ FastAPI backend server
- 🖥️ Streamlit frontend with real-time updates
- ✅ Git-integrated project with branches for modular development

---

## 🧠 Tech Stack

| Layer     | Tool       |
|-----------|------------|
| Frontend  | [Streamlit]|
| Backend   | [FastAPI]|
| Language  | Python 3.10+ |
| Hashing   | `hashlib`, custom logic |
| Version Control | Git + GitHub |

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yaksha04/demo-MLmodel.git
cd demo-MLmodel
````

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi streamlit uvicorn watchdog
```

---

## 🏁 How to Run the App

### Start Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

The FastAPI server will run at:
📍 `http://127.0.0.1:8000`

---

### Start Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

The Streamlit app will run at:
📍 `http://localhost:8501`

---

## 🧩 API Endpoints (FastAPI)

| Method | Endpoint         | Description                         |
| ------ | ---------------- | ----------------------------------- |
| GET    | `/ping`          | Health check                        |
| GET    | `/hashstatus`    | Returns current hash per model path |
| POST   | `/notify-change` | Sends change notification (if used) |

---

## 🧪 Development Workflow

* Use `main` branch as production/stable
* Feature branches:

  * `backend-feature`: Backend changes
  * `frontend-feature`: UI/UX changes
* Use pull requests to merge into `main`
* GitHub tracks changes via commit hash and file diff

---

## 📬 Notifications

When any `id.txt` file is modified under any model path (`apple/001/L1/id.txt`, etc.), the backend updates the **combined hash** and optionally notifies the frontend of a model update.

