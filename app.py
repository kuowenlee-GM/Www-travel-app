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
            if "季節物品" not in st.session_state.ITEM_DATABASE: st.session_state.ITEM_DATABASE["季節物品"] = {}
            if new_season not in st.session_state.ITEM_DATABASE["季節物品"]: st.session_state.ITEM_DATABASE["季節物品"][new_season] = []
            st.session_state.ITEM_DATABASE["季節物品"][new_season].append(new_item)
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()

# --- 主畫面 ---
st.title("🦔 樂樂時光機")

col1, col2, col3 = st.columns(3)
with col1: dest = st.selectbox("目的地", ["國內", "國外"])
with col2: scene = st.selectbox("場景", list(st.session_state.ITEM_DATABASE.get(dest, {}).keys()))
with col3: season = st.selectbox("季節", ["春季", "夏季", "秋季", "冬季"])

base_items = st.session_state.ITEM_DATABASE[dest].get(scene, [])
seasonal_items = st.session_state.ITEM_DATABASE.get("季節物品", {}).get(season, [])
final_list = list(set(base_items + seasonal_items))

st.subheader(f"✅ 此次打包清單")
checked_items = []
for idx, item in enumerate(final_list):
    if st.checkbox(item, key=f"{dest}_{scene}_{season}_{idx}"):
        checked_items.append(item)

# --- 存檔區 ---
st.divider()
st.subheader("💾 旅程存檔")
trip_name = st.text_input("幫這次旅程取個名字")
if st.button("儲存此次打包清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "dest": dest,
            "scene": scene,
            "season": season,
            "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success(f"旅程「{trip_name}」存檔成功！")
        st.rerun()

# --- 歷史查閱 ---
st.divider()
st.subheader("📂 瀏覽歷史打包清單")
history = st.session_state.ITEM_DATABASE.get("歷史紀錄", {})
for name, data in list(history.items()):
    with st.expander(f"📂 {name}"):
        st.write(f"**目的地**: {data.get('dest')} | **場景**: {data.get('scene')} | **季節**: {data.get('season')}")
        st.write("**帶出門的清單**:")
        for item in data.get('checked_items', []):
            st.markdown(f"- ✅ {item}")
        if st.button(f"🗑️ 刪除 {name}", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()
