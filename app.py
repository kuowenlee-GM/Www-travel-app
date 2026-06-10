import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 簡化且絕對安全的資料管理 ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {
        "國內": {"民宿": ["刷牙組", "睡衣"]}, 
        "國外": {"通用必備": ["護照"]},
        "季節": {"夏季": ["墨鏡"]},
        "歷史": {}
    }

if 'db' not in st.session_state:
    st.session_state.db = load_data()

# --- 1. 側邊欄：新增功能 ---
with st.sidebar:
    st.title("🛠 設定")
    cat = st.selectbox("分類", ["國內", "國外", "季節"])
    sub = st.text_input("子分類/名稱")
    item = st.text_input("物品")
    if st.button("加入"):
        if sub not in st.session_state.db[cat]: st.session_state.db[cat][sub] = []
        st.session_state.db[cat][sub].append(item)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.db, f, ensure_ascii=False)
        st.rerun()

# --- 2. 主畫面：打包 ---
st.title("🦔 樂樂清單")
dest = st.selectbox("目的地", ["國內", "國外"])
# 顯示選中的場景
scenes = st.multiselect("選擇場景", list(st.session_state.db[dest].keys()))

checked = []
for s in scenes:
    for i in st.session_state.db[dest][s]:
        if st.checkbox(i, key=f"b_{s}_{i}"): checked.append(i)

# 季節勾選
s_type = st.selectbox("季節", ["無", "夏季", "冬季"])
if s_type != "無":
    for i in st.session_state.db["季節"].get(s_type, []):
        if st.checkbox(f"季節: {i}", key=f"s_{i}"): checked.append(i)

# 存檔
name = st.text_input("存檔名")
if st.button("💾 存檔"):
    st.session_state.db["歷史"][name] = checked
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.db, f, ensure_ascii=False)
    st.rerun()

# 歷史紀錄
for name, items in st.session_state.db["歷史"].items():
    with st.expander(f"📁 {name}"):
        st.write(items)
        if st.button(f"刪除 {name}", key=f"d_{name}"):
            del st.session_state.db["歷史"][name]
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(st.session_state.db, f, ensure_ascii=False)
            st.rerun()
