# Www-travel-app
import streamlit as st

# 設定標題
st.title("樂樂成長時光機")

# 1、安全設定
SECRET_PASSWORD = "1224"
password = st.text_input("輸入私密密碼", type="password")

if password == SECRET_PASSWORD:
    st.success("歡迎進入樂樂的專屬小窩！")
    
    # 2、新增物品面板 (這是妳要的最高權限！)
    with st.expander("📝 總編輯管理面板"):
        new_item = st.text_input("想給樂樂新增什麼寶貝？")
        category = st.selectbox("要放在哪個分類？", ["國內", "國外"])
        if st.button("確認新增"):
            st.write(f"系統已紀錄：'{new_item}' 到 '{category}' 清單！")
            st.balloons() # 慶祝一下成功！

    # 3、清單顯示
    st.subheader("國外 - 沙灘 必備清單")
    items = ["證照", "簽證", "外幣", "轉換插頭", "保險單", "泳衣", "防曬乳", "拖鞋", "墨鏡", "遮陽帽"]
    for item in items:
        st.checkbox(item)

else:
    if password:
        st.error("密碼錯誤，請重新輸入")
