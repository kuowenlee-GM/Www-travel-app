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
                data = json.load(f)
                # --- 強制資料清洗 ---
                if not isinstance(data, dict): return default_data
                if "歷史紀錄" not in data or not isinstance(data["歷史紀錄"], dict):
                    data["歷史紀錄"] = {}
                return data
        except: return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

st.title("🦔 樂樂時光機")

# 1. 選擇場景
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 2. 顯示分區打包
all_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene} 分區")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for i, item in enumerate(items):
        st.checkbox(f"{item}", key=f"pack_{scene}_{i}")
        if item not in all_items: all_items.append(item)

# 3. 儲存紀錄
st.divider()
st.subheader("💾 旅程存檔")
trip_name = st.text_input("幫這次旅程取個名字")

if st.button("儲存此次打包清單"):
    if trip_name:
        # 強制將歷史資料結構化為字典
        if not isinstance(st.session_state.ITEM_DATABASE.get("歷史紀錄"), dict):
            st.session_state.ITEM_DATABASE["歷史紀錄"] = {}
            
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "items": all_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()

# 4. 歷史清單展示 (終極容錯版)
history = st.session_state.ITEM_DATABASE.get("歷史紀錄", {})
if isinstance(history, dict) and history:
    st.subheader("📂 瀏覽歷史打包清單")
    for name, data in list(history.items()):
        # 再次確保 data 是字典格式
        if not isinstance(data, dict): continue
        
        cols = st.columns([4, 1])
        with cols[0].expander(f"📂 {name}"):
            st.write(f"**場景**: {', '.join(data.get('scenes', []))}")
            st.write("**項目**: {', '.join(data.get('items', []))}")
        
        if cols[1].button("🗑️", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()
