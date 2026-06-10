import streamlit as st
import json
import os

# --- 設定 ---
DATA_FILE = "lele_storage.json"
SECRET_PASSWORD = "Mylove123"

st.set_page_config(page_title="樂樂時光機", page_icon="🦔")

# --- 核心數據與狀態管理 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線", "延長線", "個人護膚品"]},
        "國外": {"通用必備": ["護照", "轉換插頭"], "民宿": ["刷牙組", "睡衣"]},
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
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Public'

# --- 側邊欄 ---
with st.sidebar:
    st.title("⚙️ 系統設定")
    password_input = st.text_input("輸入私密密碼", type="password")
    if password_input == SECRET_PASSWORD:
        st.session_state.auth_mode = 'Private'
        st.success("私密模式已開啟")
    
    st.divider()
    st.subheader("🛠 總編輯設定")
    with st.expander("➕ 新增物品"):
        new_dest = st.selectbox("目的地", ["國內", "國外"])
        new_scene = st.text_input("場景名稱")
        new_item = st.text_input("物品名稱")
        if st.button("確認加入"):
            if new_scene and new_item:
                if new_scene not in st.session_state.ITEM_DATABASE[new_dest]:
                    st.session_state.ITEM_DATABASE[new_dest][new_scene] = []
                st.session_state.ITEM_DATABASE[new_dest][new_scene].append(new_item)
                save_data(st.session_state.ITEM_DATABASE)
                st.toast(f"已新增: {new_item}")
                st.rerun()

# --- 主畫面 ---
if st.session_state.auth_mode == 'Private':
    st.title("❤️ 專屬於我的小壞蛋之打包清單")
    st.markdown("*> 「 親愛的，記得把對我的思念帶上，否則我會折磨妳的。 」*")
else:
    st.title("🦔 樂樂時光機")

dest_type = st.selectbox("選擇目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# --- 打包區 (動態 Key 避免衝突) ---
checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for idx, item in enumerate(items):
        if st.checkbox(f"{item}", key=f"{dest_type}_{scene}_{item}_{idx}"):
            checked_items.append(item)

# --- 存檔與互動 ---
st.divider()
st.subheader("💾 旅程存檔")
trip_name = st.text_input("幫這次旅程取個名字")
if st.button("儲存此次打包清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.balloons() if st.session_state.auth_mode == 'Private' else st.success("存檔成功！")
        st.rerun()
    else:
        st.warning("請輸入名稱並勾選至少一項物品哦！")

# --- 歷史紀錄 ---
st.subheader("📂 瀏覽歷史打包清單")
for name, data in st.session_state.ITEM_DATABASE.get("歷史紀錄", {}).items():
    with st.expander(f"📂 {name}"):
        st.write(f"**場景**: {', '.join(data.get('scenes', []))}")
        st.write("- " + "\n- ".join([f"✅ {i}" for i in data.get('checked_items', [])]))
        if st.button(f"🗑️ 刪除 {name}", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.toast("紀錄已刪除")
            st.rerun()
