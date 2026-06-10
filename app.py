import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 絕對不會崩潰的初始化 ---
def init_db():
    return {
        "國內": {"民宿": ["刷牙組", "睡衣"]},
        "國外": {"通用必備": ["護照"]},
        "季節": {"夏季": ["墨鏡"], "冬季": ["暖暖包"]},
        "歷史": {}
    }

# 讀取並強制確保結構完整
if 'db' not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                st.session_state.db = json.load(f)
        except:
            st.session_state.db = init_db()
    else:
        st.session_state.db = init_db()

# 自動修復：如果檔案裡少了欄位，馬上補上去
defaults = init_db()
for key in defaults:
    if key not in st.session_state.db:
        st.session_state.db[key] = defaults[key]

st.title("🦔 樂樂清單")

# --- 側邊欄 ---
with st.sidebar:
    st.title("🛠 設定")
    cat = st.selectbox("分類", ["國內", "國外", "季節"])
    sub = st.text_input("子分類")
    item = st.text_input("物品")
    if st.button("加入"):
        if sub not in st.session_state.db[cat]: st.session_state.db[cat][sub] = []
        st.session_state.db[cat][sub].append(item)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.db, f, ensure_ascii=False)
        st.rerun()

# --- 主程式 ---
dest = st.selectbox("目的地", ["國內", "國外"])
scenes = st.multiselect("場景", list(st.session_state.db[dest].keys()))

checked = []
for s in scenes:
    for i in st.session_state.db[dest][s]:
        if st.checkbox(i, key=f"b_{s}_{i}"): checked.append(i)

# 季節
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

# 安全瀏覽歷史
st.divider()
if "歷史" in st.session_state.db:
    for name, items in st.session_state.db["歷史"].items():
        with st.expander(f"📁 {name}"):
            st.write(items)
            if st.button(f"刪除 {name}", key=f"d_{name}"):
                del st.session_state.db["歷史"][name]
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(st.session_state.db, f, ensure_ascii=False)
                st.rerun()
