import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 1. 數據管理 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "季節物品": {"春季": ["薄外套"], "夏季": ["墨鏡"], "秋季": ["圍巾"], "冬季": ["發熱衣"]},
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

# --- 2. 側邊欄 ---
with st.sidebar:
    st.title("⚙️ 總編輯中心")
    # [新增與刪除區塊略，保持你原本正常運作的那一段]
    
    st.divider()
    st.title("📜 歷史紀錄")
    history = st.session_state.ITEM_DATABASE.get("歷史紀錄", {})
    for trip_name, items in history.items():
        with st.expander(f"🧳 {trip_name}"):
            st.write(", ".join(items))
            if st.button(f"刪除 {trip_name}", key=f"del_h_{trip_name}"):
                del st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name]
                save_data(st.session_state.ITEM_DATABASE)
                st.rerun()

# --- 3. 主畫面 ---
st.title("🦔 樂樂時光機")

# 目的地與場景 (key 必須獨立)
dest_main = st.selectbox("目的地", ["國內", "國外"], key="dest_main")
scenes = list(st.session_state.ITEM_DATABASE.get(dest_main, {}).keys())
selected_scenes = st.multiselect("選擇場景", scenes, key="scene_main")

checked_items = []
# 打包區
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    for item in st.session_state.ITEM_DATABASE[dest_main].get(scene, []):
        if st.checkbox(item, key=f"pack_{scene}_{item}"):
            checked_items.append(item)

# 季節區 (重點：key 與其他分開)
st.subheader("🍂 季節補強")
season = st.selectbox("選擇季節", ["無", "春季", "夏季", "秋季", "冬季"], key="season_select")
if season != "無":
    for item in st.session_state.ITEM_DATABASE["季節物品"].get(season, []):
        if st.checkbox(f"季節: {item}", key=f"season_{item}"):
            checked_items.append(item)

st.divider()
trip_name = st.text_input("輸入紀錄名稱")
if st.button("💾 儲存清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = checked_items
        save_data(st.session_state.ITEM_DATABASE)
        st.success("已存檔！")
        st.rerun()
