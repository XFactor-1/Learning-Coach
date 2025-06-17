# learning_coach_mvp.py
# 🎯 MVP for Personal AI Learning Coach

import streamlit as st
import sqlite3
from datetime import datetime

# --- DB Setup --- #
conn = sqlite3.connect("learning_progress.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        date TEXT,
        topic TEXT,
        self_rating INTEGER,
        confidence INTEGER,
        notes TEXT
    )
''')
conn.commit()

# --- UI --- #
st.title("📘 AI 個人學習教練 MVP")
st.markdown("讓你追蹤每日進度，並自動統整學習歷程。")

# --- Form Input --- #
st.subheader("📅 今日學習紀錄")
with st.form("log_form"):
    today = datetime.today().strftime('%Y-%m-%d')
    topic = st.text_input("今天學了什麼？（例如：LangChain Tools、Python class...）")
    self_rating = st.slider("掌握程度（0-100）", 0, 100, 50)
    confidence = st.slider("信心程度（0-100）", 0, 100, 50)
    notes = st.text_area("備註 / 問題 / 下次複習建議")
    submitted = st.form_submit_button("✅ 儲存")
    if submitted and topic:
        c.execute("INSERT INTO progress VALUES (?, ?, ?, ?, ?)",
                  (today, topic, self_rating, confidence, notes))
        conn.commit()
        st.success("已儲存！")

# --- Progress Viewer --- #
st.subheader("📊 歷史紀錄")
progress = c.execute("SELECT * FROM progress ORDER BY date DESC").fetchall()
for p in progress:
    st.markdown(f"**📅 {p[0]}** | 主題：{p[1]} | 掌握度：{p[2]} | 信心：{p[3]}\n\n📝 {p[4]}")

conn.close()
