import streamlit as st
import random
import time

# --- 画面設定 ---
st.set_page_config(page_title="スマホで神経衰弱", layout="centered")
st.title("🃏 スマホで神経衰弱")

# --- 設定：12枚（3列×4行） ---
COLS = 3  # 横に3枚
ROWS = 4  # 縦に4行
TOTAL_CARDS = COLS * ROWS

# --- データ管理 ---
if 'cards' not in st.session_state:
    nums = list(range(1, (TOTAL_CARDS // 2) + 1)) * 2
    random.shuffle(nums)
    st.session_state.cards = nums
    st.session_state.opened = [False] * TOTAL_CARDS
    st.session_state.selected = []
    st.session_state.cleared = False

# --- ゲーム画面（ここが修正ポイント！） ---
# st.columns(COLS) をループの外で1回だけ作る
cols = st.columns(COLS)

for i in range(TOTAL_CARDS):
    # i % COLS を使うことで、0, 1, 2 番目のカラムに順番に配置される
    with cols[i % COLS]:
        if st.session_state.opened[i]:
            st.button(f" {st.session_state.cards[i]} ", key=f"card_{i}", disabled=True, use_container_width=True)
        else:
            if st.button("❓", key=f"card_{i}", use_container_width=True):
                if len(st.session_state.selected) < 2:
                    st.session_state.opened[i] = True
                    st.session_state.selected.append(i)
                    st.rerun()

# --- 判定ロジック ---
if len(st.session_state.selected) == 2:
    i1, i2 = st.session_state.selected
    if st.session_state.cards[i1] == st.session_state.cards[i2]:
        st.toast("正解！🎉")
        st.session_state.selected = []
    else:
        st.toast("ハズレ！")
        time.sleep(1.0)
        st.session_state.opened[i1] = False
        st.session_state.opened[i2] = False
        st.session_state.selected = []
        st.rerun()

# --- クリア演出 ---
if all(st.session_state.opened) and not st.session_state.cleared:
    st.session_state.cleared = True
    st.balloons()
    st.success("おめでとう！全部クリア！🎊")

if st.button("リセット"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
