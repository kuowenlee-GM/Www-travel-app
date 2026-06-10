import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "Mylove123"

st.set_page_config(page_title="樂樂時光機", page_icon="🦔")

# --- 數據管理 (加入防禦性結構修復) ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線"], "沙灘": ["泳衣", "防曬乳", "拖鞋", "遮陽帽"]},
        "國外": {"通用必備": ["護照", "轉換插頭"], "民宿": ["刷牙組", "睡衣"]},
        "季節物品": {
            "春季": ["薄外套", "雨傘"],
            "夏季": ["墨鏡", "防曬噴霧", "手持電風扇"],
            "秋季": ["薄長袖", "圍巾"],
            "冬季": ["發熱衣", "暖暖包", "厚外套", "毛帽"]
        },
        "歷史紀錄": {}
    }
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 確保讀取到的資料包含所有必要的鍵，否則補上預設值
                if not isinstance(data, dict): return default_data
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                return data
        except: return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 側邊欄 ---
with st.sidebar:
    st.title("⚙️ 系統設定")
    if st.text_input("輸入私密密碼", type="password") == SECRET_PASSWORD:
        st.session_state.auth_mode = 'Private'
    
    st.divider()
    st.subheader("🛠 總編輯")
    if st.expander("➕ 新增季節小物"):
        new_season = st.selectbox("選擇季節", ["春季", "夏季", "秋季", "冬季"])
        new_item = st.text_input("物品名稱")
        if st.button("確認加入"):
            # 確保季節物品存在
            if "季節物品" not in st.session_state.ITEM_DATABASE:
                st.session_state.ITEM_DATABASE["季節物品"] = {}
            if new_season not in st.session_state.ITEM_DATABASE["季節物品"]:
                st.session_state.ITEM_DATABASE["季節物品"][new_season] = []
            
            st.session_state.ITEM_DATABASE["季節物品"][new_season].append(new_item)
            save_data(st.session_state.ITEM_DATABASE)
            st.toast(f"已加入: {new_item}")
            st.rerun()

# --- 主畫面 ---
st.title("🦔 樂樂時光機")
if st.session_state.get('auth_mode') == 'Private':
    st.markdown("❤️ *親愛的，記得把對我的思念帶上...*")

col1, col2, col3 = st.columns(3)
with col1: dest = st.selectbox("目的地", ["國內", "國外"])
with col2: scene = st.selectbox("場景", list(st.session_state.ITEM_DATABASE.get(dest, {}).keys()))
with col3: season = st.selectbox("季節", ["春季", "夏季", "秋季", "冬季"])

# --- 生成清單邏輯 ---
base_items = st.session_state.ITEM_DATABASE[dest].get(scene, [])
# 安全讀取季節物品，如果沒有該季節則回傳空列表
seasonal_items = st.session_state.ITEM_DATABASE.get("季節物品", {}).get(season, [])
final_list = list(set(base_items + seasonal_items))

st.subheader(f"✅ 此次打包清單 ({dest} / {scene} / {season})")

checked_items = []
for idx, item in enumerate(final_list):
    if st.checkbox(item, key=f"{dest}_{scene}_{season}_{idx}"):
        checked_items.append(item)

# --- 歷史存檔 ---
st.divider()
st.subheader("💾 旅程存檔")
trip_name = st.text_input("給這次旅程取個名字")
if st.button("儲存打包清單"):
    if trip_name and checked_items:
        if "歷史紀錄" not in st.session_state.ITEM_DATABASE:
            st.session_state.ITEM_DATABASE["歷史紀錄"] = {}
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": [scene], "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()
