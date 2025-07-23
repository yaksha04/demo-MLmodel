from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pathlib import Path
import hashlib

app = FastAPI()

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Point to the MLmodel directory one level above
BASE_PATH = Path(__file__).resolve().parent.parent
current_hash = None

def compute_model_hash():
    hash_md5 = hashlib.md5()
    for file in sorted(BASE_PATH.rglob("id.txt")):
        hash_md5.update(file.read_bytes())
    return hash_md5.hexdigest()

@app.get("/commodities")
def list_commodities() -> List[str]:
    return sorted([d.name for d in BASE_PATH.iterdir()
                   if d.is_dir() and d.name not in ["backend", "frontend"]])

@app.get("/versions/{commodity}")
def list_versions(commodity: str) -> List[str]:
    path = BASE_PATH / commodity
    return sorted([d.name for d in path.iterdir() if d.is_dir()])

@app.get("/layers/{commodity}/{version}")
def list_layers(commodity: str, version: str) -> List[str]:
    path = BASE_PATH / commodity / version
    return sorted([d.name for d in path.iterdir() if d.is_dir()])

@app.get("/id/{commodity}/{version}/{layer}")
def get_id(commodity: str, version: str, layer: str):
    file_path = BASE_PATH / commodity / version / layer / "id.txt"
    if file_path.exists():
        return {"content": file_path.read_text()}
    else:
        return {"error": "id.txt not found"}

@app.get("/model/hash")
def get_model_hash():
    global current_hash
    new_hash = compute_model_hash()
    changed = new_hash != current_hash
    current_hash = new_hash
    return {"hash": new_hash, "changed": changed}
