import streamlit as st
import random
import time

# --- 画面設定 ---
st.set_page_config(page_title="スマホで神経衰弱・豪華版", layout="centered")
st.title("🃏 スマホで神経衰弱")

# --- 設定：枚数を増やす ---
# 18枚（9ペア）にする：ROWS * COLS = 18 になるように調整
ROWS, COLS = 6, 3 # 6行3列（スマホで見やすい縦長構成）
TOTAL_CARDS = ROWS * COLS

# --- データ管理（セッション） ---
if 'cards' not in st.session_state:
    # 1〜9の数字をペアで作成
    nums = list(range(1, (TOTAL_CARDS // 2) + 1)) * 2
    random.shuffle(nums)
    st.session_state.cards = nums
    st.session_state.opened = [False] * TOTAL_CARDS
    st.session_state.selected = []
    st.session_state.cleared = False # クリア判定用

# --- ゲーム画面（カードを並べる） ---
cols = st.columns(COLS)
for i in range(TOTAL_CARDS):
    with cols[i % COLS]:
        if st.session_state.opened[i]:
            st.button(f" {st.session_state.cards[i]} ", key=f"card_{i}", disabled=True)
        else:
            if st.button("❓", key=f"card_{i}"):
                if len(st.session_state.selected) < 2:
                    st.session_state.opened[i] = True
                    st.session_state.selected.append(i)
                    st.rerun()

# --- 2枚選んだ後の判定 ---
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

# --- 全問正解（クリア）の判定 ---
if all(st.session_state.opened) and not st.session_state.cleared:
    st.session_state.cleared = True
    st.balloons() # 🎈 風船を飛ばす！
    st.success("おめでとう！全部クリアしたよ！🎊")

# リセットボタン
if st.button("ゲームをリセットする"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
