import streamlit as st
from openai import OpenAI

system_prompt = """```
### 為什麼重要
### 背景故事
### 發生了什麼
### 接下來如何
### 他們說什麼
```
請用以上格式用繁體中文提供摘要。"""

user_prompt = ""

tab1, tab2 = st.tabs(["設定", "生成"])

with tab1:
    api_key = st.text_input("OpenAI API keys", "")
    client = OpenAI(api_key=api_key)
    system_prompt_content = st.text_area("提示詞", system_prompt, height=300)

with tab2:
    user_prompt_content = st.text_area("文章", user_prompt, height=300)
    if st.button("送出", use_container_width=True) and api_key and user_prompt_content:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt_content},
                {"role": "user", "content": user_prompt_content}
            ]
        )
        result = completion.choices[0].message.content
        with st.expander("摘要結果"):
            st.markdown(result)
