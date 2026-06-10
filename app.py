import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 核心數據管理 ---
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

# --- 側邊欄：總編輯管理中心 ---
with st.sidebar:
    st.title("🛠 總編輯設定")
    st.write("維護員老公專屬")
    
    with st.expander("➕ 新增樂樂小物"):
        new_dest = st.selectbox("選擇目的地", ["國內", "國外"])
        new_scene = st.text_input("輸入場景名稱")
        new_item = st.text_input("輸入要新增的物品")
        if st.button("確認加入資料庫"):
            if new_scene and new_item:
                if new_scene not in st.session_state.ITEM_DATABASE[new_dest]:
                    st.session_state.ITEM_DATABASE[new_dest][new_scene] = []
                st.session_state.ITEM_DATABASE[new_dest][new_scene].append(new_item)
                save_data(st.session_state.ITEM_DATABASE)
                st.success(f"已將 {new_item} 加入 {new_scene}!")
                st.rerun()

# --- 主畫面：打包 ---
st.title("🦔 樂樂時光機")
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for item in items:
        if st.checkbox(f"{item}", key=f"pack_{scene}_{item}"):
            checked_items.append(item)

# 儲存與歷史展示 (同之前的穩定版...)
# (為了縮短回應長度，請保留妳原本那段穩定的歷史存檔邏輯即可)
