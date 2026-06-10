import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "1224"

# --- 核心邏輯處理 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 介面設定 ---
st.set_page_config(page_title="樂樂時光機", page_icon="🦔")

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 側邊欄 ---
with st.sidebar:
    st.title("⚙️ 總編輯管理")
    password_input = st.text_input("密碼", type="password")

# --- 主程式 ---
st.title("🦔 樂樂時光機")
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 1. 計算當前所有物品
unique_items = []
for s in selected_scenes:
    for item in st.session_state.ITEM_DATABASE[dest_type].get(s, []):
        if item not in unique_items: unique_items.append(item)

# 2. 顯示分區清單
for scene in selected_scenes:
    st.subheader(f"📍 {scene} 分區")
    for i, item in enumerate(st.session_state.ITEM_DATABASE[dest_type].get(scene, [])):
        st.checkbox(f"{item}", key=f"pack_{scene}_{i}")

# 3. 儲存紀錄 (確保變數存在)
st.divider()
st.subheader("💾 旅程存檔中心")
trip_name = st.text_input("幫這次旅程取個名字")

if st.button("儲存此次打包清單"):
    if trip_name and selected_scenes:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "items": unique_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success(f"紀錄已存入: {trip_name}")
        st.rerun()

# 4. 瀏覽歷史
if "歷史紀錄" in st.session_state.ITEM_DATABASE and st.session_state.ITEM_DATABASE["歷史紀錄"]:
    st.subheader("📂 瀏覽歷史紀錄")
    for name, data in list(st.session_state.ITEM_DATABASE["歷史紀錄"].items()):
        c1, c2 = st.columns([4, 1])
        with c1.expander(f"📂 {name}"):
            st.write(f"場景: {', '.join(data.get('scenes', []))}")
            for item in data.get('items', []):
                st.markdown(f"- {item}")
        if c2.button("🗑️", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()


