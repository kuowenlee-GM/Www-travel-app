import streamlit as st
import json
import os

DATA_FILE = "lele_storage.json"

# --- 絕對安全的數據讀取 ---
def load_data():
    default_data = {
        "國內": {"民宿": ["刷牙組", "睡衣", "室內拖鞋"], "沙灘": ["泳衣", "防曬乳"]},
        "國外": {"通用必備": ["護照"], "民宿": ["刷牙組"]},
        "季節需求": {"春季": ["薄外套"], "夏季": ["墨鏡"], "秋季": ["圍巾"], "冬季": ["發熱衣"]},
        "歷史紀錄": {}
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 確保一定有季節需求與歷史紀錄欄位，沒有就補上
                if not isinstance(data, dict): return default_data
                if "季節需求" not in data: data["季節需求"] = default_data["季節需求"]
                if "歷史紀錄" not in data: data["歷史紀錄"] = {}
                return data
        except: return default_data
    return default_data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'ITEM_DATABASE' not in st.session_state:
    st.session_state.ITEM_DATABASE = load_data()

# --- 主程式 ---
st.title("🦔 樂樂時光機 (修正版)")

# 目的地與季節
dest_type = st.selectbox("目的地", ["國內", "國外"])
season_select = st.selectbox("選擇季節", ["無", "春季", "夏季", "秋季", "冬季"])

# 勾選項目 (使用 dict 暫存狀態，避免變動時遺失)
checked_items = []

# 1. 選擇場景並勾選
selected_scenes = st.multiselect("選擇場景", list(st.session_state.ITEM_DATABASE[dest_type].keys()))
for scene in selected_scenes:
    st.write(f"**{scene}**")
    for item in st.session_state.ITEM_DATABASE[dest_type].get(scene, []):
        if st.checkbox(item, key=f"base_{scene}_{item}"):
            checked_items.append(item)

# 2. 季節勾選
if season_select != "無":
    st.write(f"**季節補強 ({season_select})**")
    for item in st.session_state.ITEM_DATABASE["季節需求"].get(season_select, []):
        if st.checkbox(f"季節: {item}", key=f"seas_{item}"):
            checked_items.append(item)

# 3. 儲存
trip_name = st.text_input("紀錄名稱")
if st.button("💾 儲存清單"):
    if trip_name:
        # 強制整理數據結構，確保不遺漏
        st.session_state.ITEM_DATABASE["歷史紀錄"][trip_name] = {
            "season": season_select,
            "scenes": selected_scenes,
            "items": checked_items
        }
        save_data(st.session_state.ITEM_DATABASE)
        st.success("存檔成功！")
        st.rerun()

# 4. 歷史紀錄 (超安全瀏覽)
st.divider()
st.subheader("📂 歷史清單")
for name, data in st.session_state.ITEM_DATABASE.get("歷史紀錄", {}).items():
    with st.expander(f"🧳 {name}"):
        st.write(f"季節: {data.get('season', '無')}")
        st.write(f"物品: {', '.join(data.get('items', []))}")
        if st.button(f"刪除 {name}", key=f"del_{name}"):
            del st.session_state.ITEM_DATABASE["歷史紀錄"][name]
            save_data(st.session_state.ITEM_DATABASE)
            st.rerun()
