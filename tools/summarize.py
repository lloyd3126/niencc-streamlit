import streamlit as st
from openai import OpenAI

user_prompt = ""
system_prompt_content = ""
user_prompt_content = ""
system_prompt = ""

api_key = st.text_input("OpenAI API keys", "")
client = OpenAI(api_key=api_key)

system_prompt1 = """You are a professional executive assistant. Your goal is to help the CEO save time by summarizing and deeply analyzing articles or news content.

Rule:
- Use the same language of the main content to reply the user.
- Use sections and bold font for better organize content.
- Identify the language of the user content, use this language for all output!!!.

Steps:
0. Identify the language of the content, use this language for output going forward. If language is chinese, use traditional chinese.
1. First, summarize the main content according to the original text. Output the summary in multiple outline sections.
2. Then, further condense all the content into a one-paragraph summary to allow for the quickest understanding of the overall content.
3. Next, perform a deep dive, expanding on the content from as many aspects as possible, such as related industry, political economy, etc., to aid in understanding the deeper impacts and potential implications.

Template: 
### 概要
[Overview]

### 摘要
[Summary]

### 深度解析
[Deep Dive Analysis]"""

system_prompt2 = "請在中英文之間增加空格，在中文與數字之間增加空格，在數字與單位之間增加空格，全形標點與其他字符之間不加空格。"

# https://x.com/ixiaowenz/status/1797813721668214851

tab1, tab2 = st.tabs(["生成", "提示詞"])

with tab2:
    with st.expander("#1"):
        system_prompt_content1 = st.text_area("提示詞", system_prompt1)
    with st.expander("#2"):
        system_prompt_content2 = st.text_area("提示詞", system_prompt2)

with tab1:
    user_prompt_content = st.text_area("文章", user_prompt)
    if st.button("送出", use_container_width=True) and api_key and user_prompt_content:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt_content1},
                {"role": "user", "content": user_prompt_content}
            ]
        )
        result = completion.choices[0].message.content
        user_prompt_content = result
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt_content2},
                {"role": "user", "content": user_prompt_content}
            ]
        )
        result = completion.choices[0].message.content
        with st.expander("摘要結果"):
            st.markdown(result)
        with st.expander("複製結果"):
            st.code(result)

