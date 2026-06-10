import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 1. 數據管理 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "季節物品": {"春季": ["薄外套"], "夏季": ["墨鏡"]},
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

# --- 2. 側邊欄：總編輯中心 & 歷史管理 ---
with st.sidebar:
    st.title("⚙️ 總編輯中心")
    
    with st.expander("➕ 新增物品"):
        cat = st.selectbox("分類", ["國內", "國外", "季節物品"])
        sub = st.text_input("子分類")
        item = st.text_input("物品名稱")
        if st.button("確認加入"):
            if cat not in st.session_state.ITEM_DATABASE: st.session_state.ITEM_DATABASE[cat] = {}
            if sub not in st.session_state.ITEM_DATABASE[cat]: st.session_state.ITEM_DATABASE[cat][sub] = []
            st.session_state.ITEM_DATABASE[cat][sub].append(item)
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()

    with st.expander("🗑️ 刪除物品"):
        del_cat = st.selectbox("分類", ["國內", "國外", "季節物品"])
        del_sub = st.selectbox("子分類", list(st.session_state.ITEM_DATABASE.get(del_cat, {}).keys()))
        del_item = st.selectbox("選擇物品", st.session_state.ITEM_DATABASE.get(del_cat, {}).get(del_sub, []))
        if st.button("確認刪除"):
            st.session_state.ITEM_DATABASE[del_cat][del_sub].remove(del_item)
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()

    st.divider()
    st.title("📜 歷史打包清單")
    # 顯示歷史清單
    history = st.session_state.ITEM_DATABASE.get("歷史紀錄", {})
    if history:
        for trip_name, items in history.items():
            with st.expander(f"🧳 {trip_name}"):
                st.write(", ".join(items))
                if st.button(f"刪除 {trip_name}", key=f"del_{trip_name}"):
                    del st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name]
                    save_data(st.session_state.ITEM_DATABASE)
                    st.rerun()
    else:
        st.info("尚無儲存的清單")

# --- 3. 主畫面 ---
st.title("🦔 樂樂時光機")
dest_type = st.selectbox("目的地", ["國內", "國外"])
scenes = list(st.session_state.ITEM_DATABASE.get(dest_type, {}).keys())
selected_scenes = st.multiselect("選擇場景", scenes)

checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    for item in st.session_state.ITEM_DATABASE[dest_type].get(scene, []):
        if st.checkbox(item, key=f"pack_{scene}_{item}"):
            checked_items.append(item)

st.divider()
trip_name = st.text_input("為這次打包命名")
if st.button("💾 儲存打包清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = checked_items
        save_data(st.session_state.ITEM_DATABASE)
        st.success(f"清單「{trip_name}」已存入歷史紀錄！")
        st.rerun()
    else:
        st.warning("請輸入名字並至少勾選一個物品")
