import streamlit as st
import os
import shutil
import ffmpeg
from datetime import datetime
from openai import OpenAI

api_key = st.text_input("OpenAI API keys", "")
client = OpenAI(api_key=api_key)

language = st.text_input("transcript language", "zh")

user_prompt1 = """使用繁體中文與英文輸出。"""
user_prompt1 = st.text_area("轉逐字稿的提示詞", user_prompt1) + "\n\n"


# 創建文件上傳器
uploaded_file = st.file_uploader(
    "文件上傳器", 
    type=["mp3","mp4","mpeg","mpga","m4a","wav","webm"]
)

def check_file_size(file_path, max_size_mb=24):
    # 將 MB 轉換為 Bytes
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # 獲取檔案大小
    file_size = os.path.getsize(file_path)
    
    # 檢查檔案大小是否超過限制
    if file_size > max_size_bytes:
        print(f"檔案 {file_path} 大小為 {file_size / (1024 * 1024):.2f} MB，超過 {max_size_mb} MB 的限制。")
        return False
    else:
        print(f"檔案 {file_path} 大小為 {file_size / (1024 * 1024):.2f} MB，在限制範圍內。")
        return True

if uploaded_file is not None:
    # 讀取檔名
    full_file_name = uploaded_file.name
    # full_file_name = full_file_name.replace(' ', '_')
    file_extension = os.path.splitext(full_file_name)[1]
    file_name = os.path.splitext(full_file_name)[0]
    st.session_state.file_name = file_name

    # 匯入檔案
    # 1. 準備匯入目錄
    # 2. 將檔案複製到目錄
    current_timestamp = datetime.now().timestamp()
    current_timestamp = str(current_timestamp).split(".")[0]
    input_dir = f"./input/{current_timestamp}"
    os.makedirs(input_dir, exist_ok=True)
    source_path = os.path.join(input_dir, full_file_name)
    f = open(source_path, "wb")
    f.write(uploaded_file.getbuffer())
    st.write('')
    st.write(f'1 / 3 - 檔案複製到此資料夾下')

    # 處理檔案 1
    # 1. 準備輸出目錄
    # 2. 轉換並壓縮檔案
    output_dir = f"./output/{current_timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    input_file = f'{input_dir}/{full_file_name}'
    output_file = f'{output_dir}/{file_name}.mp3'
    st.write(f'2 / 3 - 轉換並壓縮檔案')
    ffmpeg.input(input_file).output(output_file, q='9', ac='1').overwrite_output().run()

    if check_file_size(output_file):

        # 處理檔案 2
        # 1. 轉換成 srt 格式的逐字稿
        input_file = open(output_file, "rb")
        output_file = f'{output_dir}/{file_name}.srt'
        st.write(f'3 / 3 - 轉換成 srt 格式的逐字稿')
        prompt = user_prompt1
        transcription = client.audio.transcriptions.create(
            model = "whisper-1", 
            file = input_file,
            language = language,
            response_format="srt",
            prompt = prompt
        )
        file = open(output_file, 'w')
        file.write(transcription)
        with st.expander("逐字稿 - srt 格式"):
            st.code(transcription, language='wiki')
        with st.expander("逐字稿 - text 格式"):
            transcription_txt = ""
            for idx, t in enumerate(transcription.split("\n")):
                if idx % 4 == 2:
                    transcription_txt += t + " "
            st.code(transcription_txt, language='wiki')

    else:
        st.write(f'超過檔案大小')

    shutil.rmtree("./input")
    shutil.rmtree("./output")

