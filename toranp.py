import streamlit as st
import random
import time

# --- 1. 画面設定 ---
st.set_page_config(page_title="神経衰弱", layout="centered")

# --- 2. 【最重要】スマホでも横並びを強制する魔法のCSS ---
st.markdown('''
    <style>
    /* 1. カラムの横並びをスマホでも維持する */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 0px !important; /* 隙間を調整 */
    }
    /* 2. 各カラムの幅をスマホでも33%（3列）に固定する */
    div[data-testid="column"] {
        flex: 1 1 30% !important;
        min-width: 30% !important;
        max-width: 33% !important;
    }
    /* 3. ボタンの文字を大きく、高さを出して押しやすくする */
    .stButton>button {
        height: 80px !important;
        font-size: 24px !important;
        margin-bottom: 5px !important;
    }
    </style>
''', unsafe_allow_html=True)

# タイトル
st.title("🃏 神経衰弱")

# --- 3. ゲーム設定（12枚：3列×4行） ---
COLS = 3
ROWS = 4
TOTAL_CARDS = COLS * ROWS

# --- 4. データ管理（セッション状態） ---
if 'cards' not in st.session_state:
    # 1〜6の数字をペアで作成
    nums = list(range(1, (TOTAL_CARDS // 2) + 1)) * 2
    random.shuffle(nums)
    st.session_state.cards = nums
    st.session_state.opened = [False] * TOTAL_CARDS
    st.session_state.selected = []
    st.session_state.cleared = False

# --- 5. ゲーム画面（カード配置） ---
cols = st.columns(COLS)

for i in range(TOTAL_CARDS):
    with cols[i % COLS]:
        if st.session_state.opened[i]:
            # めくられた後の数字
            st.button(f"{st.session_state.cards[i]}", key=f"card_{i}", disabled=True, use_container_width=True)
        else:
            # 伏せられたカード
            if st.button("❓", key=f"card_{i}", use_container_width=True):
                if len(st.session_state.selected) < 2:
                    st.session_state.opened[i] = True
                    st.session_state.selected.append(i)
                    st.rerun()

# --- 6. 判定ロジック ---
if len(st.session_state.selected) == 2:
    i1, i2 = st.session_state.selected
    if st.session_state.cards[i1] == st.session_state.cards[i2]:
        st.toast("正解！🎉")
        st.session_state.selected = []
    else:
        st.toast("ハズレ！")
        time.sleep(0.6) # スマホでテンポ良く遊べるよう少し短縮
        st.session_state.opened[i1] = False
        st.session_state.opened[i2] = False
        st.session_state.selected = []
        st.rerun()

# --- 7. クリア演出 ---
if all(st.session_state.opened) and not st.session_state.cleared:
    st.session_state.cleared = True
    st.balloons() # 🎈 風船が飛ぶ
    st.success("おめでとう！全部クリアしたよ！🎊")

# --- 8. リセット ---
if st.button("ゲームをリセット"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
