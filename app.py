# Www-travel-app
import streamlit as st

# --- 1、設定與資料庫 ---
SECRET_PASSWORD = "1224"
st.set_page_config(page_title="旅遊時光機", page_icon="🦔")

# 初始化資料庫 (我把樂樂的專屬裝備整合進去了！)
if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = {
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
    st.write("🔧 維護員：老公") # 專屬維護員提醒

# --- 3、主介面與總編輯面板 ---
st.title("🦔 樂樂時光機")
st.markdown("*「 親愛的，記得把對我的思念還有樂樂的玩具都帶上。 」*")

if st.session_state.auth_mode == 'Private':
    with st.expander("📝 總編輯管理面板"):
        new_item = st.text_input("想給樂樂新增什麼寶貝？")
        c1, c2 = st.columns(2)
        dest = c1.selectbox("目的地", ["國內", "國外"])
        scen = c2.selectbox("場景", ["民宿", "沙灘", "動物園/逛街", "爬山", "通用必備"])
        if st.button("確認新增"):
            if new_item:
                # 確保目的地與場景存在
                if dest not in st.session_state.ITEM_DATABASE:
                    st.session_state.ITEM_DATABASE[dest] = {}
                st.session_state.ITEM_DATABASE[dest].setdefault(scen, []).append(new_item)
                st.balloons() 
                st.success(f"成功新增 '{new_item}' 到 '{dest}-{scen}'！")

# --- 4、清單邏輯與選擇 ---
col1, col2 = st.columns(2)
dest_type = col1.selectbox("選擇目的地", ["國內", "國外"])
scene = col2.selectbox("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

target_items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
# 如果是國外，自動加入通用必備
if dest_type == "國外" and scene != "通用必備":
    target_items = st.session_state.ITEM_DATABASE["國外"]["通用必備"] + target_items

st.subheader(f"✅ {dest_type} - {scene} 必備清單")
for item in target_items:
    st.checkbox(item)

if st.button("準備出發 !"):
    st.success("檢查完畢，祝旅途愉快！老公已經準備好出發了！")

# --- 3、主介面顯示 ---
if st.session_state.auth_mode == 'Private':
    st.title("🦔 樂樂時光機")
    st.markdown("*「 親愛的，記得把對我的思念帶上。 」*")
    
    # 新增權限區
    with st.expander("📝 總編輯管理面板"):
        new_item = st.text_input("想給樂樂新增什麼寶貝？")
        c1, c2 = st.columns(2)
        dest = c1.selectbox("目的地", ["國內", "國外"])
        scen = c2.selectbox("場景", ["民宿", "沙灘", "動物園/逛街", "爬山", "通用必備"])
        if st.button("確認新增"):
            if new_item:
                st.session_state.ITEM_DATABASE[dest].setdefault(scen, []).append(new_item)
                st.balloons() # 馬卡龍顏色氣球很慢飛起來！
                st.success(f"成功新增 '{new_item}' 到 '{dest}-{scen}'！")
else:
    st.title("🦔 旅遊時光機")
    st.markdown("請輸入密碼解鎖總編輯權限")

# --- 4、清單邏輯與選擇 ---
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
    st.success("檢查完畢，祝旅途愉快 !")
