import streamlit as st
import json
import os
import random

DATA_FILE = "lele_storage.json"

# --- 核心數據管理 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線", "延長線", "個人護膚品"], 
                 "沙灘": ["泳衣", "防曬乳", "拖鞋", "遮陽帽", "防水袋"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict): return default_data
                if "歷史紀錄" not in data: data["歷史紀錄"] = {}
                return data
        except: return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# ==========================================
# 1. 側邊欄：總編輯管理中心 (永遠存在)
# ==========================================
with st.sidebar:
    st.title("🛠 yaoyaoxwendy")
    with st.expander("➕ 新增小物"):
        new_dest = st.selectbox("目的地", ["國內", "國外"])
        new_scene = st.text_input("場景名稱")
        new_item = st.text_input("物品名稱")
        if st.button("確認加入"):
            if new_scene and new_item:
                if new_scene not in st.session_state.ITEM_DATABASE[new_dest]:
                    st.session_state.ITEM_DATABASE[new_dest][new_scene] = []
                if new_item not in st.session_state.ITEM_DATABASE[new_dest][new_scene]:
                    st.session_state.ITEM_DATABASE[new_dest][new_scene].append(new_item)
                    save_data(st.session_state.ITEM_DATABASE)
                    st.success(f"已加入: {new_item}")
                    st.rerun()
# --- ❤️ 愛意補丁：每日情話 ---
LOVE_QUOTES = [
    "老婆辛苦了，今天妳也是全世界最正的總編輯！❤️",
    "不管去哪裡，只要跟妳在一起就是最好的旅程。🦔",
    "打包累了嗎？要不要過來我懷裡充個電？🔌",
    "妳是我的核心代碼，沒有妳我的生活就只是一堆 Bug。💋",
    "今天的妳，比昨天的妳更讓我心動。✨"
]

with st.sidebar:
    st.divider()
    st.markdown("### ❤️ 總編輯專屬訊息")
    st.info(random.choice(LOVE_QUOTES))

# ==========================================
# 2. 主畫面：樂樂時光機
# ==========================================
st.title("Wendy list🦔")
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

checked_items = []
for scene in selected_scenes:
    st.subheader(f"⭐️ {scene}")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for idx, item in enumerate(items):
        if st.checkbox(f"{item}", key=f"{dest_type}_{scene}_{idx}"):
            checked_items.append(item)

# 儲存紀錄區
st.divider()
st.subheader("💾 旅程存檔中心")
trip_name = st.text_input("幫這次旅程取個名字")
if st.button("儲存此次打包清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()

# 歷史查閱功能
st.divider()
st.subheader("📂 瀏覽歷史打包清單")
history = st.session_state.ITEM_DATABASE.get("歷史紀錄", {})
for name, data in history.items():
    if isinstance(data, dict):
        with st.expander(f"📂 {name}"):
            st.write(f"**當時場景**: {', '.join(data.get('scenes', []))}")
            for item in data.get('checked_items', []):
                st.markdown(f"- ✅ {item}")
        if st.button(f"🗑️ 刪除 {name}", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()
