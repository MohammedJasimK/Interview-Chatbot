# # streamlit_app.py
#
# import streamlit as st
# import random
# import pickle
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Load saved model and data
# vectorizer = pickle.load(open(r"C:\Users\jasim\Data Science\My Project\Interview Chatbot\model\vectorizer.pkl", "rb"))
# df = pickle.load(open(r"C:\Users\jasim\Data Science\My Project\Interview Chatbot\model\qa_data.pkl", "rb"))
#
# st.title("🎯 Interview Preparation Chatbot")
# st.write("Practice your Python, SQL, ML, NLP, and Generative AI interview questions!")
#
# # Sidebar
# topic = st.sidebar.selectbox("Select Topic", df['Topic'].unique())
# difficulty = st.sidebar.selectbox("Select Difficulty", df['Difficulty'].unique())
#
# # Get question
# if "question" not in st.session_state:
#     st.session_state.question = None
#     st.session_state.answer = None
#
# if st.button("🧠 Get Question"):
#     filtered = df[(df['Topic'] == topic) & (df['Difficulty'] == difficulty)]
#     if not filtered.empty:
#         row = filtered.sample(1).iloc[0]
#         st.session_state.question = row['Question']
#         st.session_state.answer = row['Answer']
#         st.session_state.clean_answer = row['clean_answer']
#     else:
#         st.warning("No questions found for this selection!")
#
# if st.session_state.question:
#     st.subheader("💭 Question:")
#     st.write(st.session_state.question)
#
#     user_answer = st.text_area("✍️ Your Answer:")
#     if st.button("Check Answer"):
#         if user_answer.strip() == "":
#             st.warning("Please enter your answer first.")
#         else:
#             user_clean = user_answer.lower()
#             answers = [user_clean, st.session_state.clean_answer]
#             vectors = vectorizer.transform(answers)
#             sim = cosine_similarity(vectors[0], vectors[1])[0][0]
#
#             if sim > 0.75:
#                 st.success(f"✅ Correct! (Similarity: {sim:.2f})")
#             elif sim > 0.4:
#                 st.info(f"🟡 Almost correct! (Similarity: {sim:.2f})")
#             else:
#                 st.error(f"❌ Incorrect! (Similarity: {sim:.2f})")
#
#             with st.expander("💡 Show Correct Answer"):
#                 st.write(st.session_state.answer)



import streamlit as st
import random
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# PAGE CONFIG
st.set_page_config(
    page_title="Interview Preparation Chatbot",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f5ffff;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .title {
        color: #1f77b4;
        text-align: center;
        font-size: 38px;
        font-weight: bold;
    }
    .subtitle {
        color: #333333;
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }
    .question-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        font-size: 17px;
        margin-top: 10px;
    }
    .answer-box {
        background-color: #f1f8e9;
        padding: 15px;
        border-radius: 10px;
        font-size: 16px;
    }
    .feedback {
        font-size: 16px;
        font-weight: bold;
        padding: 10px;
        margin-top: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# LOAD MODEL
vectorizer = pickle.load(open(r"C:\Users\jasim\Data Science\My Project\Interview Chatbot\model\vectorizer.pkl", "rb"))
df = pickle.load(open(r"C:\Users\jasim\Data Science\My Project\Interview Chatbot\model\qa_data.pkl", "rb"))

# HEADER
st.markdown("<h1 class='title'>Interview Preparation Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Practice Python, SQL, ML, NLP, and Generative AI Interview Questions — Improve your confidence!</p>", unsafe_allow_html=True)
st.write("")

# SIDEBAR
with st.sidebar:
    st.header("Customize Practice")
    topic = st.selectbox("Select Topic", df['Topic'].unique())
    difficulty = st.selectbox("Select Difficulty",df['Difficulty'].unique(),)
    st.markdown("---")
    st.markdown("*Tip: Try different topics and levels to challenge yourself!*")

# SESSION STATE
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.answer = None
    st.session_state.clean_answer = None
    st.session_state.score = 0
    st.session_state.total = 0

# FUNCTION TO GET QUESTION
def get_question(topic, difficulty):
    filtered = df[(df['Topic'] == topic) & (df['Difficulty'] == difficulty)]
    if not filtered.empty:
        row = filtered.sample(1).iloc[0]
        return row['Question'], row['Answer'], row['clean_answer']
    else:
        return None, None, None

# MAIN APP
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("Get New Question", use_container_width=True):
        q, a, ca = get_question(topic, difficulty)
        if q:
            st.session_state.question = q
            st.session_state.answer = a
            st.session_state.clean_answer = ca
        else:
            st.warning("No questions found for the selected topic and difficulty.")

    if st.session_state.question:
        st.markdown(f"<div class='question-box'><b> Question:</b> {st.session_state.question}</div>", unsafe_allow_html=True)
        user_answer = st.text_area(" Type your answer here:", key="user_input", height=120)

        if st.button("Check Answer", use_container_width=True):
            if not user_answer.strip():
                st.warning("Please write your answer before checking!")
            else:
                answers = [user_answer.lower(), st.session_state.clean_answer]
                vectors = vectorizer.transform(answers)
                sim = cosine_similarity(vectors[0], vectors[1])[0][0]

                st.session_state.total += 1

                if sim > 0.60:
                    st.session_state.score += 1
                    st.success(f"Correct! Great job! (Similarity: {sim:.2f})")
                elif sim > 0.30:
                    st.session_state.score += 0.5
                    st.info(f"Almost correct! (Similarity: {sim:.2f})")
                elif sim > 0.15:
                    st.warning(f"Need Improvement! (Similarity: {sim:.2f})")
                else:
                    st.error(f"Incorrect. Keep practicing! (Similarity: {sim:.2f})")

                with st.expander("Show Correct Answer"):
                    st.markdown(f"<div class='answer-box'>{st.session_state.answer}</div>", unsafe_allow_html=True)

    # SCORE & PROGRESS
    if st.session_state.total > 0:
        progress = st.session_state.score / st.session_state.total
        st.markdown("---")
        st.markdown(f"**Score:** {st.session_state.score}/{st.session_state.total}")
        st.progress(progress)
