import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 核心數據管理：加入唯一性檢查 ---
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
                return data if isinstance(data, dict) else default_data
        except: return default_data
    return default_data

def save_data(data):
    # 存檔前做一次清洗：移除場景中重複的物品
    for dest in data:
        if dest == "歷史紀錄": continue
        for scene in data[dest]:
            data[dest][scene] = list(dict.fromkeys(data[dest][scene])) # 移除重複
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 側邊欄：總編輯管理中心 ---
with st.sidebar:
    st.title("🛠 總編輯設定")
    with st.expander("➕ 新增樂樂小物"):
        new_dest = st.selectbox("目的地", ["國內", "國外"])
        new_scene = st.text_input("場景名稱")
        new_item = st.text_input("物品名稱")
        # 增加「防止重複點擊」的按鈕邏輯
        if st.button("確認加入資料庫"):
            if new_scene and new_item:
                if new_scene not in st.session_state.ITEM_DATABASE[new_dest]:
                    st.session_state.ITEM_DATABASE[new_dest][new_scene] = []
                # 只有不在裡面才加
                if new_item not in st.session_state.ITEM_DATABASE[new_dest][new_scene]:
                    st.session_state.ITEM_DATABASE[new_dest][new_scene].append(new_item)
                    save_data(st.session_state.ITEM_DATABASE)
                    st.success(f"已加入: {new_item}")
                    st.rerun() # 強制重整畫面，確保不會重複送出
                else:
                    st.warning("這個物品已經在清單裡了唷！")

# --- 主畫面 ---
st.title("🦔 樂樂時光機")
dest_type = st.selectbox("目的地", ["國內", "國外"])
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))

# 打包勾選區
checked_items = []
for scene in selected_scenes:
    st.subheader(f"📍 {scene}")
    items = st.session_state.ITEM_DATABASE[dest_type].get(scene, [])
    for idx, item in enumerate(items):
        if st.checkbox(f"{item}", key=f"{dest_type}_{scene}_{idx}"):
            checked_items.append(item)

# 儲存紀錄區
st.divider()
st.subheader("💾 旅程存檔")
trip_name = st.text_input("旅程名稱", key="trip_name_input")
if st.button("儲存此次清單"):
    if trip_name and checked_items:
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "scenes": selected_scenes,
            "checked_items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()
