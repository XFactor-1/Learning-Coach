
import streamlit as st
import openai
import os

# GPT 建議函式
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt_suggestion(completed_lessons, difficulty):
    prompt = f'''
你是一位個人學習教練。使用者目前學習進度如下：
- 完成課程ID：{completed_lessons}
- 目前難度等級：{difficulty}
請根據這些資訊，提供一段100字以內的建議，幫助使用者下一步該學什麼，如何有效進步。
'''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ 無法取得建議：{e}"

# 模擬課程資料
lessons = [
    {"id": 1, "title": "AI PM - 基礎職責", "difficulty": 1},
    {"id": 2, "title": "AI PM - 資料驅動產品設計", "difficulty": 2},
    {"id": 3, "title": "AI PM - AI倫理與風險管理", "difficulty": 3},
    {"id": 4, "title": "Python - 變數與資料型態", "difficulty": 1},
    {"id": 5, "title": "Python - 函式與流程控制", "difficulty": 2},
    {"id": 6, "title": "Python - 資料處理實務", "difficulty": 3},
]

# 使用者進度
if "difficulty" not in st.session_state:
    st.session_state.difficulty = 1
if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = []

st.title("🎓 個人學習教練")

st.sidebar.header("🧠 目前設定")
st.sidebar.write(f"目前難度：{st.session_state.difficulty}")
st.sidebar.write("已完成課程：", st.session_state.completed_lessons)

# 推薦課程
st.header("📚 推薦課程")
recommended = [l for l in lessons if l["difficulty"] == st.session_state.difficulty and l["id"] not in st.session_state.completed_lessons]
if not recommended:
    st.info("🎉 你已完成此難度的課程，將為你提升難度！")
    if st.session_state.difficulty < 3:
        st.session_state.difficulty += 1
    recommended = [l for l in lessons if l["difficulty"] == st.session_state.difficulty and l["id"] not in st.session_state.completed_lessons]

for lesson in recommended:
    if st.button(f"完成課程：{lesson['title']}"):
        st.session_state.completed_lessons.append(lesson["id"])
        st.experimental_rerun()

# GPT 建議區塊
st.header("🤖 GPT 學習建議")

if st.button("獲取 GPT 建議"):
    suggestion = get_gpt_suggestion(
        st.session_state.completed_lessons,
        st.session_state.difficulty
    )
    st.success(suggestion)
