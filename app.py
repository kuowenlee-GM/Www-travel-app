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

# --- 2. 側邊欄 ---
with st.sidebar:
    st.title("⚙️ 總編輯中心")
    
    with st.expander("➕ 新增物品"):
        # 修改標籤避免衝突
        cat_edit = st.selectbox("選擇分類 (編輯)", ["國內", "國外", "季節物品"], key="cat_edit")
        sub_edit = st.text_input("子分類名稱", key="sub_edit")
        item_edit = st.text_input("物品名稱", key="item_edit")
        if st.button("確認加入"):
            if cat_edit not in st.session_state.ITEM_DATABASE: st.session_state.ITEM_DATABASE[cat_edit] = {}
            if sub_edit not in st.session_state.ITEM_DATABASE[cat_edit]: st.session_state.ITEM_DATABASE[cat_edit][sub_edit] = []
            st.session_state.ITEM_DATABASE[cat_edit][sub_edit].append(item_edit)
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()

    with st.expander("🗑️ 刪除物品"):
        del_cat = st.selectbox("刪除分類 (編輯)", ["國內", "國外", "季節物品"], key="del_cat")
        del_sub = st.selectbox("刪除子分類 (編輯)", list(st.session_state.ITEM_DATABASE.get(del_cat, {}).keys()), key="del_sub")
        del_item = st.selectbox("選擇物品 (編輯)", st.session_state.ITEM_DATABASE.get(del_cat, {}).get(del_sub, []), key="del_item")
        if st.button("確認刪除"):
            st.session_state.ITEM_DATABASE[del_cat][del_sub].remove(del_item)
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()

    st.divider()
    st.title("📜 歷史打包紀錄")
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
dest_main = st.selectbox("目的地 (主畫面)", ["國內", "國外"], key="dest_main")
scenes = list(st.session_state.ITEM_DATABASE.get(dest_main, {}).keys())
selected_scenes = st.multiselect("選擇場景 (主畫面)", scenes, key="scene_main")

checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    for item in st.session_state.ITEM_DATABASE[dest_main].get(scene, []):
        if st.checkbox(item, key=f"pack_{scene}_{item}"):
            checked_items.append(item)

st.divider()
trip_name = st.text_input("儲存名稱")
if st.button("💾 儲存打包清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = checked_items
        save_data(st.session_state.ITEM_DATABASE)
        st.success("已存檔！")
        st.rerun()
