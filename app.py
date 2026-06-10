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
                # 確保資料結構完整
                if not isinstance(data, dict): return default_data
                if "歷史紀錄" not in data: data["歷史紀錄"] = {}
                return data
        except: return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 主畫面：打包 ---
st.title("🦔 樂樂時光機")
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for idx, item in enumerate(items):
        # 使用唯一Key
        if st.checkbox(f"{item}", key=f"{dest_type}_{scene}_{idx}"):
            checked_items.append(item)

# --- 儲存紀錄區 ---
st.divider()
st.subheader("💾 旅程存檔中心")
trip_name = st.text_input("幫這次旅程取個名字")

if st.button("儲存此次打包清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()

# --- 歷史查閱功能 (徹底修復版) ---
st.divider()
st.subheader("📂 瀏覽歷史打包清單")
history = st.session_state.ITEM_DATABASE.get("歷史紀錄", {})

if not history:
    st.info("目前還沒有存檔紀錄唷！")
else:
    for name, data in history.items():
        # 確保 data 是字典格式，避免崩潰
        if isinstance(data, dict):
            with st.expander(f"📂 {name}"):
                scenes = data.get("scenes", [])
                items = data.get("checked_items", [])
                st.write(f"**當時場景**: {', '.join(scenes) if isinstance(scenes, list) else scenes}")
                st.write("**帶出門的清單**:")
                for item in items:
                    st.markdown(f"- ✅ {item}")
            
            if st.button(f"🗑️ 刪除 {name}", key=f"del_{name}"):
                del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
                save_data(st.session_state.ITEM_DATABASE)
                st.rerun()
