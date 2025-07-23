from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pathlib import Path
import hashlib

app = FastAPI()

# Allow Streamlit frontend to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Base path points one level up from the backend folder
BASE_PATH = Path(__file__).resolve().parent.parent
current_hash = None

# ✅ Compute hash from all id.txt files
def compute_model_hash():
    hash_md5 = hashlib.md5()
    for file in sorted(BASE_PATH.rglob("id.txt")):
        hash_md5.update(file.read_bytes())
    return hash_md5.hexdigest()

# ✅ List top-level commodity directories (e.g., apple, mango)
@app.get("/commodities")
def list_commodities() -> List[str]:
    return sorted([
        d.name for d in BASE_PATH.iterdir()
if d.is_dir()
        and not d.name.startswith(".")               # 🔒 exclude hidden dirs like .git
        and d.name not in {"backend", "frontend"}    # 🔒 exclude app code folders
    ])

# ✅ List versions inside a commodity (e.g., 001, 002)
@app.get("/versions/{commodity}")
def list_versions(commodity: str) -> List[str]:
    path = BASE_PATH / commodity
    if not path.exists():
        return []
    return sorted([
        d.name for d in path.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])

# ✅ List layers inside a version (e.g., L1, L2)
@app.get("/layers/{commodity}/{version}")
def list_layers(commodity: str, version: str) -> List[str]:
    path = BASE_PATH / commodity / version
    if not path.exists():
        return []
    return sorted([
        d.name for d in path.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])

# ✅ Read the content of id.txt
@app.get("/id/{commodity}/{version}/{layer}")
def get_id(commodity: str, version: str, layer: str):
file_path = BASE_PATH / commodity / version / layer / "id.txt"
    if file_path.exists():
        return {"content": file_path.read_text()}
    else:
        return {"error": "id.txt not found"}

# ✅ Return current hash of all id.txt files + change status
@app.get("/model/hash")
def get_model_hash():
    global current_hash
    new_hash = compute_model_hash()
    changed = new_hash != current_hash
    current_hash = new_hash
    return {"hash": new_hash, "changed": changed}
