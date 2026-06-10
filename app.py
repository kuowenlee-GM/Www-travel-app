import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# 1. 讀取數據：強制確保結構完整，避免 KeyError
def load_data():
    default = {
        "國內": {"民宿": ["刷牙組", "睡衣"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"]},
        "季節": {"夏季": ["墨鏡"], "冬季": ["暖暖包"]},
        "歷史": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 自動補齊缺少的欄位
                for key in default:
                    if key not in data: data[key] = default[key]
                return data
        except: return default
    return default

if 'db' not in st.session_state:
    st.session_state.db = load_data()

st.title("🦔 樂樂清單：紀錄顯示版")

# --- 側邊欄：新增功能 ---
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

# --- 主程式：選擇 ---
dest = st.selectbox("目的地", ["國內", "國外"])
scenes = st.multiselect("場景", list(st.session_state.db[dest].keys()))
s_type = st.selectbox("季節", ["無", "夏季", "冬季"])

# --- 存檔區 ---
name = st.text_input("幫這次打包取個名字")
if st.button("💾 儲存清單"):
    # 這裡我們把選取的場景與季節都存進去
    st.session_state.db["歷史"][name] = {
        "場景": scenes,
        "季節": s_type
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.db, f, ensure_ascii=False)
    st.success("存檔成功！")
    st.rerun()

# --- 歷史顯示區 (不會崩潰版) ---
st.divider()
st.subheader("📂 歷史紀錄")
for name, info in st.session_state.db["歷史"].items():
    with st.expander(f"📁 {name}"):
        # 使用 .get 安全地取得內容，沒資料就顯示「無」
        scenes_str = ', '.join(info.get("場景", [])) if info.get("場景") else "無"
        season_str = info.get("季節", "無")
        
        st.write(f"**場景**: {scenes_str}")
        st.write(f"**季節**: {season_str}")
        
        if st.button(f"刪除 {name}", key=f"d_{name}"):
            del st.session_state.db["歷史"][name]
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(st.session_state.db, f, ensure_ascii=False)
            st.rerun()
