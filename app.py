import streamlit as st
import json
import os

# --- 1、設定與檔案處理 ---
DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "1224"

def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="樂樂時光機", page_icon="🦔")

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 2、側邊欄與管理 ---
with st.sidebar:
    st.title("⚙️ 總編輯管理")
    password_input = st.text_input("密碼", type="password")
    if password_input == SECRET_PASSWORD:
        st.session_state.auth_mode = 'Private'
    st.divider()
    st.write("🔧 維護員：老公")

# --- 3、主介面與打包邏輯 ---
st.title("🦔 樂樂時光機")
dest_type = st.selectbox("目的地", ["國內", "國外"])
scenes = st.multiselect("場景 (可複選)", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 整理清單並去重
unique_items = []
for s in scenes:
    items = st.session_state.ITEM_DATABASE[dest_type].get(s, [])
    for item in items:
        if item not in unique_items: unique_items.append(item)

# 顯示打包區
st.subheader("✅ 綜合打包清單")
for i, item in enumerate(unique_items):
    st.checkbox(item, key=f"pack_{i}")

# --- 4、歷史紀錄中心 ---
st.divider()
st.subheader("💾 旅程存檔中心")
trip_name = st.text_input("幫這次旅程取個名字")

if st.button("儲存此次打包清單"):
    if trip_name:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": scenes,
            "items": unique_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success(f"紀錄已存入: {trip_name}")
        st.rerun()

# 顯示歷史紀錄 (極簡美學版)
if "歷史紀錄" in st.session_state.ITEM_DATABASE and st.session_state.ITEM_DATABASE["歷史紀錄"]:
    st.subheader("📂 瀏覽歷史打包清單")
    for name, data in st.session_state.ITEM_DATABASE["歷史紀錄"].items():
        c1, c2 = st.columns([4, 1]) 
        
        # 展開查看詳情
        with c1.expander(f"📂 {name}"):
            st.write(f"**場景**: {', '.join(data['scenes'])}")
            st.write("**清單內容**:")
            for item in data['items']:
                st.markdown(f"- {item}")
        
        # 刪除鈕在最右邊
        if c2.button("🗑️", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()

