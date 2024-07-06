import streamlit as st

introduction = st.Page("about/introduction.py", title="作者介紹", icon=":material/dashboard:", default=True)
transcriber = st.Page("tools/transcriber.py", title="生成逐字稿", icon=":material/speech_to_text:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")

pg = st.navigation(
    {
        "關於": [introduction],
        "工具": [transcriber, history],
    }
)

pg.run()
