import streamlit as st
import random
import time

# --- 画面設定 ---
st.set_page_config(page_title="おそろいカード", layout="centered")
st.title("🎰 おそろいカード")

# --- データ管理（セッション） ---
if 'cards' not in st.session_state:
    # 1〜6の数字をペアで作成
    nums = list(range(1, 7)) * 2
    random.shuffle(nums)
    st.session_state.cards = nums
    st.session_state.opened = [False] * 12
    st.session_state.selected = []

# --- ゲーム画面（カードを並べる） ---
cols = st.columns(4) # 横4列
for i in range(12):
    with cols[i % 4]:
        # すでに正解したか、今めくっているカード
        if st.session_state.opened[i]:
            st.button(f" {st.session_state.cards[i]} ", key=f"card_{i}", disabled=True)
        else:
            # まだ伏せられているカード
            if st.button("❓", key=f"card_{i}"):
                if len(st.session_state.selected) < 2:
                    st.session_state.opened[i] = True
                    st.session_state.selected.append(i)
                    st.rerun()

# --- 2枚選んだ後の判定 ---
if len(st.session_state.selected) == 2:
    i1, i2 = st.session_state.selected
    # 数字が一致したか
    if st.session_state.cards[i1] == st.session_state.cards[i2]:
        st.toast("正解！🎉")
        st.session_state.selected = [] # クリア
        
        # --- ここで全クリア判定を追加 ---
        if all(st.session_state.opened):
            st.balloons()
            st.success("おめでとう！すべてのペアを見つけました！")
        # --------------------------
        
    else:
        time.sleep(1.0) # 1秒見せる
        st.session_state.opened[i1] = False
        st.session_state.opened[i2] = False
        st.session_state.selected = []
        st.rerun()

# --- リセットボタン ---
if st.button("再チャレンジする！"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()





