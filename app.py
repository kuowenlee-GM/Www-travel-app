# Www-travel-appimport streamlit as st
import json
import os

# --- 1、設定與檔案處理 ---
DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "1224"

# 載入資料庫函數
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

# 儲存資料庫函數
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="旅遊時光機", page_icon="🦔")

# 初始化資料
if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 2、安全與權限系統 ---
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Public'

with st.sidebar:
    st.title("⚙️ 系統設定")
    password_input = st.text_input("輸入私密密碼", type="password")
    if password_input == SECRET_PASSWORD:
        st.session_state.auth_mode = 'Private'
        st.success("總編輯權限已開啟")
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
                save_data(st.session_state.ITEM_DATABASE) # 關鍵：寫入檔案！
                st.balloons()
                st.success(f"成功新增 '{new_item}'！已永久保存。")

# --- 4、清單顯示 ---
col1, col2 = st.columns(2)
dest_type = col1.selectbox("選擇目的地", ["國內", "國外"])
scene = col2.selectbox("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

target_items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
if dest_type == "國外" and scene != "通用必備":
    target_items = st.session_state.ITEM_DATABASE["國外"]["通用必備"] + target_items

st.subheader(f"✅ {dest_type} - {scene} 必備清單")
for item in target_items:
    st.checkbox(item)

if st.button("準備出發 !"):
    st.success("檢查完畢，祝旅途愉快！")


