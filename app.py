import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "Mylove123"

st.set_page_config(page_title="樂樂時光機", page_icon="🦔")

# --- 數據管理 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線"], "沙灘": ["泳衣", "防曬乳", "拖鞋", "遮陽帽"]},
        "國外": {"通用必備": ["護照", "轉換插頭"], "民宿": ["刷牙組", "睡衣"]},
        "季節物品": {
            "春季": ["薄外套", "雨傘"], "夏季": ["墨鏡", "防曬噴霧"],
            "秋季": ["薄長袖", "圍巾"], "冬季": ["發熱衣", "暖暖包"]
        },
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict): return default_data
                for key in default_data:
                    if key not in data: data[key] = default_data[key]
                return data
        except: return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 側邊欄：總編輯功能 ---
with st.sidebar:
    st.title("⚙️ 總編輯中心")
    
    # 1. 新增功能
    with st.expander("➕ 新增物品"):
        cat = st.selectbox("分類", ["國內", "國外", "季節物品"])
        sub = st.text_input("子分類 (如：民宿/夏季)")
        item = st.text_input("物品名稱")
        if st.button("確認加入"):
            if cat not in st.session_state.ITEM_DATABASE: st.session_state.ITEM_DATABASE[cat] = {}
            if sub not in st.session_state.ITEM_DATABASE[cat]: st.session_state.ITEM_DATABASE[cat][sub] = []
            st.session_state.ITEM_DATABASE[cat][sub].append(item)
            save_data(st.session_state.ITEM_DATABASE)
            st.success(f"已加入 {item}")
            st.rerun()

    # 2. 刪除功能 (推薦方式)
    with st.expander("🗑️ 刪除物品"):
        del_cat = st.selectbox("選擇要刪除的分類", ["國內", "國外", "季節物品"])
        del_sub = st.selectbox("選擇子分類", list(st.session_state.ITEM_DATABASE.get(del_cat, {}).keys()))
        del_item = st.selectbox("選擇要刪除的物品", st.session_state.ITEM_DATABASE.get(del_cat, {}).get(del_sub, []))
        
        if st.button("確認刪除"):
            st.session_state.ITEM_DATABASE[del_cat][del_sub].remove(del_item)
            save_data(st.session_state.ITEM_DATABASE)
            st.warning(f"已刪除 {del_item}")
            st.rerun()

# --- 主畫面 ---
st.title("🦔 樂樂時光機")
# (這裡放入你原本的打包邏輯...)
