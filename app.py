import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# 1. 確保數據結構永遠是最新的，沒有殘留舊欄位
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"]},
        "季節": {"夏季": ["墨鏡"], "冬季": ["暖暖包"]},
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_data
    return default_data

# 初始化
if 'db' not in st.session_state:
    st.session_state.db = load_data()

st.title("🦔 樂樂清單")

# --- 主畫面 ---
dest = st.selectbox("目的地", ["國內", "國外"])
scenes = st.multiselect("場景", list(st.session_state.db[dest].keys()))

checked = []
for s in scenes:
    for item in st.session_state.db[dest][s]:
        if st.checkbox(item, key=f"base_{s}_{item}"):
            checked.append(item)

# 季節
s_type = st.selectbox("季節", ["無", "夏季", "冬季"])
if s_type != "無":
    for item in st.session_state.db["季節"][s_type]:
        if st.checkbox(f"季節: {item}", key=f"seas_{item}"):
            checked.append(item)

# 存檔 (極簡化，不使用複雜的 get)
name = st.text_input("存檔名稱")
if st.button("💾 儲存"):
    if name:
        st.session_state.db["歷史紀錄"][name] = checked
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.db, f, ensure_ascii=False)
        st.success("成功！")
        st.rerun()

# 歷史瀏覽 (移除了所有可能出錯的複雜判斷)
st.divider()
for name, items in st.session_state.db["歷史紀錄"].items():
    with st.expander(f"📁 {name}"):
        st.write(items)
        if st.button(f"刪除 {name}", key=f"del_{name}"):
            del st.session_state.db["歷史紀錄"][name]
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(st.session_state.db, f, ensure_ascii=False)
            st.rerun()
