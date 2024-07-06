import streamlit as st

introduction = st.Page("about/introduction.py", title="作者介紹", icon=":material/dashboard:", default=True)
transcriber = st.Page("tools/transcriber.py", title="生成逐字稿", icon=":material/speech_to_text:")
summarize = st.Page("tools/summarize.py", title="生成摘要", icon=":material/summarize:")

pg = st.navigation(
    {
        "關於": [introduction],
        "工具": [transcriber, summarize],
    }
)

pg.run()
