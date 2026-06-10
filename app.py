import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 數據庫存取 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線", "延長線", "個人護膚品"], 
                 "沙灘": ["泳衣", "防曬乳", "拖鞋", "遮陽帽", "防水袋"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else default_data
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

# 2. 顯示並勾選項目
checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for item in items:
        # 使用唯一Key防止紅字
        if st.checkbox(f"{item}", key=f"{dest_type}_{scene}_{item}"):
            checked_items.append(item)

# 3. 儲存功能 (修復這裡)
st.divider()
st.subheader("💾 旅程存檔中心")
trip_name = st.text_input("幫這次旅程取個名字 (例如: 202606宜蘭)")

if st.button("儲存此次打包清單"):
    if trip_name and checked_items:
        if "歷史紀錄" not in st.session_state.ITEM_DATABASE:
            st.session_state.ITEM_DATABASE["歷史紀錄"] = {}
            
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()

# 4. 歷史清單展示 (修復這裡，穩定讀取)
if "歷史紀錄" in st.session_state.ITEM_DATABASE:
    st.divider()
    st.subheader("📂 瀏覽歷史打包清單")
    history = st.session_state.ITEM_DATABASE["歷史紀錄"]
    
    for name, data in history.items():
        with st.expander(f"📂 {name}"):
            # 安全讀取資料，避免崩潰
            scenes = data.get("scenes", [])
            items = data.get("checked_items", [])
            
            st.write(f"**當時場景**: {', '.join(scenes)}")
            st.write("**帶出門的清單**:")
            for item in items:
                st.markdown(f"- ✅ {item}")
        
        if st.button(f"🗑️ 刪除 {name}", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()
