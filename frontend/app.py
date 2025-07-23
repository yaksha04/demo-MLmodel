import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
import time

API_URL = "http://localhost:8000"

# ⏱️ Refresh every 10 seconds
st_autorefresh(interval=10 * 1000, key="model_check")

# Session state for hash tracking
if "last_hash" not in st.session_state:
    st.session_state.last_hash = None
if "update_detected" not in st.session_state:
    st.session_state.update_detected = False

# Get model hash from backend
def get_model_hash():
    try:
        res = requests.get(f"{API_URL}/model/hash")
        res.raise_for_status()
        return res.json().get("hash")
    except Exception as e:
        st.error(f"❌ Failed to fetch model hash: {e}")
        return None

# Compare hash
current_hash = get_model_hash()
if current_hash:
    if st.session_state.last_hash and current_hash != st.session_state.last_hash:
        st.session_state.update_detected = True
    st.session_state.last_hash = current_hash

# Notification
if st.session_state.update_detected:
    st.warning("🔔 A Model has been updated!")

# Fetch data from backend
def get_data(endpoint):
    try:
        res = requests.get(f"{API_URL}/{endpoint}")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"❌ API Error at /{endpoint}: {e}")
        return []

# UI
st.title("Model Version Update Notification System")

commodities = get_data("commodities")
commodity = st.selectbox("Select Commodity", commodities) if commodities else None

if commodity:
    versions = get_data(f"versions/{commodity}")
    version = st.selectbox("Select Version", versions) if versions else None
else:
    version = None

if version:
    layers = get_data(f"layers/{commodity}/{version}")
    layer = st.selectbox("Select Layer", layers) if layers else None
else:
    layer = None

# Show id.txt content
if layer:
    id_info = get_data(f"id/{commodity}/{version}/{layer}")
    if isinstance(id_info, dict) and "content" in id_info:
        st.subheader("The demo Content")
        st.code(id_info["content"], language="text")
    elif "error" in id_info:
        st.error(id_info["error"])
o

