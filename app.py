import streamlit as st

# 我們直接在程式裡寫死內容，不讀取任何檔案，保證不會有 KeyError
data = {
    "國內": {
        "民宿": ["刷牙組", "睡衣", "室內拖鞋", "充電線", "個人護膚品"],
        "沙灘": ["泳衣", "防曬乳", "拖鞋", "遮陽帽", "防水袋"]
    },
    "國外": {
        "通用必備": ["護照"],
        "民宿": ["刷牙組"]
    },
    "季節補強": {
        "夏季": ["墨鏡", "防曬噴霧"],
        "冬季": ["發熱衣", "暖暖包"]
    }
}

st.title("🦔 樂樂清單 (純淨版)")

# 選擇目的地
dest = st.selectbox("目的地", ["國內", "國外"])

# 選擇場景 (自動對應目的地)
scenes = st.multiselect("選擇場景", list(data[dest].keys()))

# 勾選項目
checked = []
for s in scenes:
    st.subheader(f"📍 {s}")
    for item in data[dest][s]:
        if st.checkbox(item, key=f"base_{s}_{item}"):
            checked.append(item)

# 選擇季節
season = st.selectbox("選擇季節", ["無", "夏季", "冬季"])
if season != "無":
    st.subheader(f"🍂 {season} 補強")
    for item in data["季節補強"][season]:
        if st.checkbox(f"季節: {item}", key=f"seas_{item}"):
            checked.append(item)

# 顯示最終清單 (直接顯示，不存檔)
st.divider()
st.subheader("✅ 你的打包清單")
if checked:
    for item in checked:
        st.write(f"• {item}")
else:
    st.write("目前尚未勾選任何物品")
