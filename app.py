import streamlit as st
import json
import os

# --- 1、設定與檔案處理 ---
DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "1224"

def load_data():
    default_data = {
        "國內": {
            "民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線", "延長線", "個人護膚品"],
            "沙灘": ["泳衣", "防曬乳", "拖鞋", "遮陽帽", "防水袋", "挖沙玩具", "遮陽帳篷"],
            "動物園/逛街": ["舒適步行鞋", "隨身水壺", "行動電源", "小雨傘", "外套", "恐龍玩具", "集章本"],
            "爬山": ["登山鞋", "快乾衣", "高能量零食", "急救小藥包", "防蚊液", "畫畫本"]
        },
        "國外": {
            "通用必備": ["證照", "簽證", "外幣", "轉換插頭", "保險單"],
            "民宿": ["刷牙組", "睡衣", "充電線"],
            "沙灘": ["泳衣", "防曬乳", "拖鞋", "墨鏡", "遮陽帽", "挖沙玩具"],
            "動物園/逛街": ["舒適步行鞋", "行動電源", "小雨傘", "恐龍玩具"],
            "爬山": ["登山鞋", "快乾衣", "高能量零食"]
        }
    }
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="旅遊時光機", page_icon="🦔")

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 2、權限與側邊欄 ---
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Public'

with st.sidebar:
    st.title("⚙️ 系統設定")
    password_input = st.text_input("輸入私密密碼", type="password")
    if password_input == SECRET_PASSWORD:
        st.session_state.auth_mode = 'Private'
    st.divider()
    st.write("🔧 維護員：老公")

# --- 3、主介面與總編輯面板 ---
st.title("🦔 樂樂時光機")

if st.session_state.auth_mode == 'Private':
    with st.expander("📝 總編輯管理面板"):
        new_item = st.text_input("想給樂樂新增什麼寶貝？")
        c1, c2 = st.columns(2)
        dest = c1.selectbox("目的地", ["國內", "國外"])
        scen = c2.selectbox("場景", list(st.session_state.ITEM_DATABASE[dest].keys()))
        if st.button("確認新增"):
            if new_item:
                st.session_state.ITEM_DATABASE[dest][scen].append(new_item)
                save_data(st.session_state.ITEM_DATABASE)
                st.balloons()
                st.success(f"成功新增 '{new_item}'！")

# --- 4、分組顯示邏輯 (總編輯專業打包版) ---
dest_type = st.selectbox("選擇目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景 (可複選)", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 根據選的場景，一個一個分組顯示
for scene in selected_scenes:
    st.subheader(f"📍 {scene} 分區裝袋清單")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    
    # 如果是國外，且選了非通用必備，自動把通用必備掛在第一個場景下
    if dest_type == "國外" and scene == selected_scenes[0] and "通用必備" not in selected_scenes:
        items = st.session_state.ITEM_DATABASE["國外"]["通用必備"] + items
    
    # 分區渲染 checkbox
    for i, item in enumerate(items):
        st.checkbox(f"{item}", key=f"{scene}_{item}_{i}")

st.divider()
if st.button("準備出發 !"):
    st.success("總編輯大人，所有分區檢查完畢，我們隨時可以出發！")
