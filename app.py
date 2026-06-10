import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# 核心邏輯：強制確保所有資料都是正確的字典格式
def load_data():
    default = {
        "國內": {"民宿": ["刷牙組", "睡衣"]},
        "國外": {"通用必備": ["護照"]},
        "季節": {"夏季": ["墨鏡"], "冬季": ["暖暖包"]},
        "歷史": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 如果讀到的不是字典，直接給預設值
                if not isinstance(data, dict): return default
                return data
        except: return default
    return default

if 'db' not in st.session_state:
    st.session_state.db = load_data()

st.title("🦔 樂樂清單：最終重置版")

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
s_type = st.selectbox("季節", ["無", "夏季", "冬季"])

# --- 存檔 ---
name = st.text_input("存檔名")
if st.button("💾 儲存"):
    st.session_state.db["歷史"][name] = {"場景": scenes, "季節": s_type}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.db, f, ensure_ascii=False)
    st.success("成功！")
    st.rerun()

# --- 安全瀏覽 (最關鍵的改動) ---
st.divider()
for name, info in st.session_state.db.get("歷史", {}).items():
    with st.expander(f"📁 {name}"):
        # 強制將 info 轉為字典，確保就算它是舊的雜亂資料也不會報錯
        if isinstance(info, dict):
            s = ', '.join(info.get("場景", [])) if isinstance(info.get("場景"), list) else "無"
            st.write(f"場景: {s}")
            st.write(f"季節: {info.get('季節', '無')}")
        else:
            st.write("紀錄格式異常，請刪除此筆。")
        
        if st.button(f"刪除 {name}", key=f"d_{name}"):
            del st.session_state.db["歷史"][name]
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(st.session_state.db, f, ensure_ascii=False)
            st.rerun()
