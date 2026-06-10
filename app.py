import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "1224"

def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣"], "沙灘": ["泳衣", "防曬乳"]},
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

# --- 側邊欄與管理 ---
with st.sidebar:
    st.title("⚙️ 總編輯管理")
    password_input = st.text_input("密碼", type="password")
    if password_input == SECRET_PASSWORD:
        st.session_state.auth_mode = 'Private'

# --- 主程式 ---
st.title("🦔 樂樂時光機")
dest_type = st.selectbox("目的地", ["國內", "國外"])
scenes = st.multiselect("場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 整理清單
unique_items = []
for s in scenes:
    items = st.session_state.ITEM_DATABASE[dest_type].get(s, [])
    for item in items:
        if item not in unique_items: unique_items.append(item)

# 顯示打包區
for i, item in enumerate(unique_items):
    st.checkbox(item, key=f"pack_{i}")

# --- 歷史紀錄與修改/刪除 ---
st.divider()
st.subheader("💾 旅程紀錄中心")
trip_name = st.text_input("旅程名稱")
if st.button("儲存紀錄"):
    st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {"scenes": scenes, "items": unique_items}
    save_data(st.session_state.ITEM_DATABASE)
    st.success("存檔成功！")

# 刪除與管理功能
if "歷史紀錄" in st.session_state.ITEM_DATABASE:
    for name in list(st.session_state.ITEM_DATABASE["歷史紀錄"].keys()):
        cols = st.columns([3, 1])
        cols[0].write(f"📂 {name}")
        if cols[1].button("刪除", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()

trip_name = st.text_input("幫這次旅程取個名字")

if st.button("儲存此次打包清單"):
    if trip_name:
        if "歷史紀錄" not in st.session_state.ITEM_DATABASE:
            st.session_state.ITEM_DATABASE["歷史紀錄"] = {}
        # 關鍵修改：不只存場景，連當時的清單內容(target_items)一起存進去！
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "items": unique_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success(f"紀錄已存入: {trip_name}")

# 顯示可以點擊的歷史紀錄
if "歷史紀錄" in st.session_state.ITEM_DATABASE and st.session_state.ITEM_DATABASE["歷史紀錄"]:
    st.subheader("📂 瀏覽歷史打包清單")
    for name, data in st.session_state.ITEM_DATABASE["歷史紀錄"].items():
        if st.button(f"查看: {name}"):
            st.info(f"當時場景: {', '.join(data['scenes'])}")
            st.write("當時清單細節:")
            st.write(data['items']) # 這裡會把當時的物品清單列出來！
