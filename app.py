import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 1. 數據加載與保存 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線"], "沙灘": ["泳衣", "防曬乳", "拖鞋"]},
        "國外": {"通用必備": ["護照", "轉換插頭"], "民宿": ["刷牙組"]},
        "季節物品": {"春季": ["薄外套"], "夏季": ["墨鏡"], "秋季": ["圍巾"], "冬季": ["發熱衣"]}
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

# --- 2. 側邊欄：總編輯中心 ---
with st.sidebar:
    st.title("⚙️ 總編輯中心")
    
    with st.expander("➕ 新增物品"):
        cat = st.selectbox("分類", ["國內", "國外", "季節物品"])
        sub = st.text_input("子分類名稱")
        item = st.text_input("物品名稱")
        if st.button("確認加入"):
            if cat not in st.session_state.ITEM_DATABASE: st.session_state.ITEM_DATABASE[cat] = {}
            if sub not in st.session_state.ITEM_DATABASE[cat]: st.session_state.ITEM_DATABASE[cat][sub] = []
            st.session_state.ITEM_DATABASE[cat][sub].append(item)
            save_data(st.session_state.ITEM_DATABASE)
            st.success("已新增！")
            st.rerun()

    with st.expander("🗑️ 刪除物品"):
        del_cat = st.selectbox("選擇分類", ["國內", "國外", "季節物品"])
        del_sub = st.selectbox("選擇子分類", list(st.session_state.ITEM_DATABASE.get(del_cat, {}).keys()))
        options = st.session_state.ITEM_DATABASE.get(del_cat, {}).get(del_sub, [])
        del_item = st.selectbox("選擇物品", options)
        if st.button("確認刪除"):
            st.session_state.ITEM_DATABASE[del_cat][del_sub].remove(del_item)
            save_data(st.session_state.ITEM_DATABASE)
            st.warning("已刪除！")
            st.rerun()

# --- 3. 主畫面：打包清單 ---
st.title("🦔 樂樂時光機")

dest_type = st.selectbox("目的地", ["國內", "國外"])
scenes = list(st.session_state.ITEM_DATABASE.get(dest_type, {}).keys())
selected_scenes = st.multiselect("選擇場景", scenes)

# 使用表單來處理勾選與存檔
with st.form("packing_form"):
    for scene in selected_scenes:
        st.subheader(f"📍 {scene} 分區")
        items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
        for item in items:
            st.checkbox(item, key=f"{dest_type}_{scene}_{item}")
    
    # 季節選項
    season = st.selectbox("季節補強", ["無", "春季", "夏季", "秋季", "冬季"])
    if season != "無":
        st.subheader(f"🍂 {season} 建議")
        for item in st.session_state.ITEM_DATABASE["季節物品"].get(season, []):
            st.checkbox(item, key=f"season_{item}")
    
    # 存檔按鈕：現在這會把狀態保存到 session_state
    submit = st.form_submit_button("保存我的打包清單狀態")
    if submit:
        st.success("清單狀態已保存！")
