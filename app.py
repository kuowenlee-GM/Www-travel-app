import streamlit as st
import json
import os

# --- 基礎設定 ---
DATA_FILE = "lele_storage.json"

def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return default_data
    return default_data

# 初始化系統
if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 主介面 ---
st.title("🦔 樂樂時光機 (核心版)")
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 顯示分區打包
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for i, item in enumerate(items):
        st.checkbox(f"{item}", key=f"pack_{scene}_{i}")

if st.button("準備出發 !"):
    st.balloons()
