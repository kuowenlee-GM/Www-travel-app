import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

def load_data():
    # 定義最乾淨的初始狀態
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
                # --- 關鍵防護：檢查資料格式是否為正確的字典 ---
                if not isinstance(data, dict) or "歷史紀錄" not in data:
                    return default_data
                return data
        except:
            return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 初始化資料
if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

st.title("🦔 樂樂時光機")

# 1. 目的地與場景
dest_type = st.selectbox("目的地", ["國內", "國外"])
# 確保資料庫結構正確
if dest_type not in st.session_state.ITEM_DATABASE:
    st.session_state.ITEM_DATABASE[dest_type] = {}
    
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 2. 打包勾選區
checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene} 分區")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for item in items:
        if st.checkbox(f"{item}", key=f"pack_{scene}_{item}"):
            checked_items.append(item)

# 3. 儲存紀錄
st.divider()
st.subheader("💾 旅程存檔")
trip_name = st.text_input("幫這次旅程取個名字")

if st.button("儲存此次打包清單"):
    if trip_name and checked_items:
        # 強制確認歷史紀錄是字典
        if not isinstance(st.session_state.ITEM_DATABASE.get("歷史紀錄"), dict):
            st.session_state.ITEM_DATABASE["歷史紀錄"] = {}
            
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()

# 4. 歷史清單展示 (防禦性顯示)
history = st.session_state.ITEM_DATABASE.get("歷史紀錄", {})
if isinstance(history, dict) and history:
    st.subheader("📂 瀏覽歷史打包清單")
    for name, data in list(history.items()):
        # 如果這筆紀錄格式跑掉，直接跳過不顯示
        if not isinstance(data, dict): continue
        
        with st.expander(f"📂 {name}"):
            st.write(f"**當時場景**: {', '.join(data.get('scenes', []))}")
            st.write("**帶出門的清單**:")
            for item in data.get("checked_items", []):
                st.markdown(f"- ✅ {item}")
        
        if st.button("🗑️ 刪除這筆紀錄",垃圾桶圖案及功能放在最右邊 key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()
