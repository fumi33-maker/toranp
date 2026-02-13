import streamlit as st
import random
import time

# --- 1. 画面設定 ---
st.set_page_config(page_title="スマホ神経衰弱", layout="centered")

# --- 2. 強力なCSS設定 ---
st.markdown('''
    <style>
    /* グリッド（網目）状に並べる設定 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* 絶対に3列 */
        gap: 10px;
        margin-bottom: 20px;
    }
    /* ボタンの見た目調整 */
    button[kind="primary"], button[kind="secondary"] {
        width: 100% !important;
        height: 80px !important;
        font-size: 24px !important;
    }
    </style>
''', unsafe_allow_html=True)

st.title("🃏 スマホで神経衰弱")

# --- 3. ゲーム設定（12枚） ---
TOTAL_CARDS = 12

if 'cards' not in st.session_state:
    nums = list(range(1, 7)) * 2
    random.shuffle(nums)
    st.session_state.cards = nums
    st.session_state.opened = [False] * TOTAL_CARDS
    st.session_state.selected = []
    st.session_state.cleared = False

# --- 4. ゲーム画面（ここが重要！） ---
# HTMLのコンテナを開始
st.markdown('<div class="grid-container">', unsafe_allow_html=True)

# 1枚ずつのボタンを配置
# grid-containerの中では columns を使わなくても CSS で 3列になります
# ただし Streamlit のボタンを HTML の中に入れるため、
# 通常の st.columns を使いつつ、CSS で強制的に横並びを維持します
cols = st.columns(3)

for i in range(TOTAL_CARDS):
    with cols[i % 3]:
        if st.session_state.opened[i]:
            st.button(f"{st.session_state.cards[i]}", key=f"c_{i}", disabled=True, use_container_width=True)
        else:
            if st.button("❓", key=f"c_{i}", use_container_width=True):
                if len(st.session_state.selected) < 2:
                    st.session_state.opened[i] = True
                    st.session_state.selected.append(i)
                    st.rerun()

# --- 5. 判定ロジック ---
if len(st.session_state.selected) == 2:
    i1, i2 = st.session_state.selected
    if st.session_state.cards[i1] == st.session_state.cards[i2]:
        st.toast("正解！🎉")
        st.session_state.selected = []
    else:
        st.toast("ハズレ！")
        time.sleep(0.5)
        st.session_state.opened[i1] = False
        st.session_state.opened[i2] = False
        st.session_state.selected = []
        st.rerun()

# --- 6. クリア演出 ---
if all(st.session_state.opened) and not st.session_state.cleared:
    st.session_state.cleared = True
    st.balloons()
    st.success("おめでとう！全部クリア！🎊")

if st.button("ゲームをリセット"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
