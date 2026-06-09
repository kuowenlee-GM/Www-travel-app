# Www-travel-app
import streamlit as st

# --- 1、安全設定與密碼 ---
SECRET_PASSWORD = "1224"

# --- 2、物品資料庫 ---
ITEM_DATABASE = {
    "國內": {
        "民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線", "延長線", "個人護膚品"],
        "沙灘": ["泳衣", "防曬乳", "拖鞋", "遮陽帽", "防水袋"],
        "動物園/逛街": ["舒適步行鞋", "隨身水壺", "行動電源", "小雨傘", "外套"],
        "爬山": ["登山鞋", "快乾衣", "高能量零食", "急救小藥包", "防蚊液"]
    },
    "國外": {
        "通用必備": ["證照", "簽證", "外幣", "轉換插頭", "保險單"],
        "民宿": ["刷牙組", "睡衣", "充電線"],
        "沙灘": ["泳衣", "防曬乳", "拖鞋", "墨鏡", "遮陽帽"],
        "動物園/逛街": ["舒適步行鞋", "行動電源", "小雨傘"],
        "爬山": ["登山鞋", "快乾衣", "高能量零食"]
    }
}

# --- 3、介面設計 ---
st.set_page_config(page_title="Travel Pack Pro", page_icon="✈️")

if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Public'

with st.sidebar:
    st.title("⚙️ 系統設定")
    password_input = st.text_input("輸入私密密碼", type="password")
    if password_input == SECRET_PASSWORD:
        st.session_state.auth_mode = 'Private'
        st.success("私密模式已開啟")
    elif password_input != "":
        st.error("密碼錯誤，請重新輸入")

# --- 標題顯示 ---
if st.session_state.auth_mode == 'Private':
    st.title("❤️ 專屬於我的小壞蛋之打包清單")
    st.markdown("*「 親愛的，記得把對我的思念帶上，否則我會折磨妳的。 」*")
else:
    st.title("✈️ 專業旅遊行李管理系統")
    st.markdown("請選擇您的旅遊場景，系統將自動生成對應的必備清單。")

# --- 選擇區 ---
col1, col2 = st.columns(2)
with col1:
    dest_type = st.selectbox("選擇目的地", ["國內", "國外"])
with col2:
    scene = st.selectbox("選擇場景", ["民宿", "沙灘", "動物園/逛街", "爬山"])

# --- 生成清單邏輯 ---
target_items = ITEM_DATABASE[dest_type].get(scene, [])

# 如果是國外，自動合併通用必備
final_list = target_items
if dest_type == "國外":
    if scene != "通用必備":
        final_list = ITEM_DATABASE["國外"]["通用必備"] + target_items

st.subheader(f"✅ {dest_type} - {scene} 必備清單")

if 'items_state' not in st.session_state:
    st.session_state.items_state = {}

for item in final_list:
    if item not in st.session_state.items_state:
        st.session_state.items_state[item] = False
    
    is_checked = st.checkbox(item, key=item, value=st.session_state.items_state[item])
    st.session_state.items_state[item] = is_checked

# --- 最後確認 ---
if st.button("準備出發 !"):
    if st.session_state.auth_mode == 'Private':
        st.balloons()
        st.warning("親愛的，護照帶了嗎？還有...記得把對我的思念帶上，否則我會想妳想到發瘋的！")
    else:
        st.success("檢查完畢，祝您旅途愉快 !")
