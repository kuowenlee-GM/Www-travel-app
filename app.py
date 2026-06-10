import streamlit as st
import json
import os

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

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

st.title("🦔 樂樂時光機")

# 1. 目的地與場景選擇
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 2. 顯示分區打包清單
all_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene} 分區")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for i, item in enumerate(items):
        st.checkbox(f"{item}", key=f"pack_{scene}_{i}")
        if item not in all_items: all_items.append(item)

# 3. 準備出發
if st.button("準備出發 !"):
    st.balloons()

# 4. 歷史紀錄中心 (加入安全性檢查)
st.divider()
st.subheader("💾 旅程存檔中心")
trip_name = st.text_input("幫這次旅程取個名字")

if st.button("儲存此次打包清單"):
    if trip_name:
        if "歷史紀錄" not in st.session_state.ITEM_DATABASE:
            st.session_state.ITEM_DATABASE["歷史紀錄"] = {}
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "items": all_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()

# 5. 瀏覽與刪除歷史
if st.session_state.ITEM_DATABASE.get("歷史紀錄"):
    st.subheader("📂 瀏覽歷史打包清單")
    for name, data in list(st.session_state.ITEM_DATABASE["歷史紀錄"].items()):
        cols = st.columns([4, 1])
        with cols[0].expander(f"📂 {name}"):
            st.write(f"場景: {', '.join(data.get('scenes', []))}")
            for item in data.get('items', []):
                st.markdown(f"- {item}")
        if cols[1].button("🗑️", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()
