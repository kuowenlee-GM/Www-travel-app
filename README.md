# Www-travel-app
t
import streamlit as stl
#--1、該心設定與愁密密碼
SECRET PASSWORD ="Mylove123" # 這裡可以改成你優我的事壓暗號！ PRIVATE_MODE -Falsel
#一2、物品資料產 （由總綸璃充的精準清單） 一 ITEM_DATABASE- (U
"國内"：[
"民宿"：["刷牙組","匯衣",「"室内挺鞋","充雹線","延長線';"個人爹5" *沙着"：「咏衣""防寝乳,`拖鞋","莘虱房;,"防水矣"遭要帽、"善市1.、 "動物園/逛街"：["舒渣步行鞋","隨身水壶","行動弯漂","小兩傘","外套", "爬山"：「"奎山鞋","快乾衣","高能量零瓮","急教小葉包,"防蚊液]
"國外"：化
"遙用必備"：[`證照","簽證","外幣","[換插頭", "保險單"]
"民宿"：["通用必慎","刷牙組","匪衣","充笔線"]'
沙瀚"：["通用必慌","泳衣","防曜乳","拖鞋""噩風晟",邃陽帽"]、 "動物團/瀣街"：["通用必沒","舒適步行鞋","行動奢漂;小兩傘"]
"爬山"：["通用必備","登山鞋","快乾衣","高能量零食"],
#--3. 介面設計 一
st.set_page_contig(page_title-"Travel Pack Pro", page _icon-""")! ン
#- 密碼切换邏輯 ..
if 'auth _mode' not in st.session_state:"
st.session._state.auth_mode- "Public'I
with st.sidebar:
sttite("@ 系统設定"） Dassword input = st.text input（"輸入愁密密礁" type="password")0 if password_input-- SECRET_PASSWORD:! st.session_state.auth_ mode = 'Private' stsuccess（"日 私密模式已開啟"） elif password _input !-""
sterrog（"密碼鉗誤,諮重新輸入"
T
#- 概題顯示 （根據模式切換）-」
if st.session_state.auth_//Mode =- 'Private':1
sttitle" I 專骚於我的小壞蛋之打包清軍"！ st. makdown（"*「 親登的,記得把對我的思念襟上,否則我會折磨妳的。 」* elseJ
ttitle("Û 事業旅遊行李管理系統" st.makdown（"請遲擇您的旅遊場景 。系統將自動生成對應的必備清單 。"！
#- 選擇區 -
col1, col2 = st.columns(2)! with col1:
destwpe - stseleclbox"挥目的地",（"氢內","园外"
with col2:1
scene = stselectbox"遥挥擇場景"[「"民宿","沙灘","動物氮/逛街","爬山"]）
T
#一 生成清單
if'items' not in st.session_state:l
st.session_state.items=
L
# 獲取對應物品
target_items ITEM_DATABASE[dest_type]-get(scene, )!
if isinstance(tarset_ items, list) and"通用必臂" in taret items: # 處理团外通用項！ tnal.lst - ITEM_DATABASE（"雯外 "["通用必饰"]+ [iforjin target items ify！-"通用必镜"]
else: final_list = target_items." っ
stsubheadeu(f" (dest bype) - (scene) 必備清單"）！ L
# 勾選邏輯'
for item in final_list: I
if item not in st.session _state.items:1 st.session_state.itemsfitem]-Falsel
# 勾選後文字變灰色且有刪除線 (SS 模影）
įs_checked = st.checkbox(item, key=item)! st.sessionstate.itemsitem]=is_checked!
if is_checked:l
st.markdgwn(f"--(item)-~~")# 簡單的視覺反諗！
#-- 最後確認視窗 一
ifst.button(",? 準備出發 !"):
if st.session_state.auth_mode-- 'Private:l st.balloons(u
stwarning("A 親爱的, 簧照蒂了嗎？還有。...記得把對我的思念帶上 , 否則我會在。
else:!
t.success("
检查完暴,祝您旅途愉快 !"[(C
