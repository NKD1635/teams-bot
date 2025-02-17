import json
import google.generativeai as genai
import time
import os
import threading
import tkinter as tk

# Geminiの設定
genai.configure(api_key="xxxxx")  # GeminiのAPIキーを取得して設定

system_content = """あなたは私のAIアシスタントです。あなたは会話の他に以下のスキルを備えています。

# 会議時の質問提示スキル
* 会議中の会話をインプットすると、3つの質問とその質問の意図を生成します。
"""
messages = [{"role": "system", "content": system_content}]

# messagesの変換用ヘルパー関数
def convert_messages(msg_list: list) -> list:
    return [m["content"] for m in msg_list]  # Gemini用に単純なリストに変換

# 前提のプロンプト
def generate_meeting_questions(meeting_text: str) -> str:
    prompt = (
        "以下の会議内容を基に、重要な点を掘り下げるための3つの質問を作成してください。"
        "また、それぞれの質問の意図を説明してください。\n"
        f"会議内容: {meeting_text}"
    )
    model = genai.GenerativeModel("gemini-pro")
    resp = model.generate_content([prompt])
    return resp.text

skills = {"generate_meeting_questions": generate_meeting_questions}

# ファイルを作成する関数（存在しない場合のみ）
def ensure_file_exists(filepath: str, initial_content: str = ""):
    try:
        with open(filepath, "x", encoding="utf-8") as file:
            file.write(initial_content)
    except FileExistsError:
        pass

# ファイルから入力を読み取る関数
def read_input_file(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        ensure_file_exists(filepath)
        return ""

# 出力をファイルに書き込む関数
def write_output_file(filepath: str, content: str):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

# ファイルの確認と作成
input_file = "input.txt"
output_file = "output.txt"
ensure_file_exists(input_file)
ensure_file_exists(output_file)

# 終了フラグ
task_running = True

def stop_program():
    global task_running
    task_running = False
    root.quit()

def generate_questions():
    text = read_input_file(input_file)
    if text:
        intent = "generate_meeting_questions"
        entities = {"meeting_text": text}
        skill = skills[intent]
        resp = skill(**entities)
        print(f"bot> {resp}")
        write_output_file(output_file, resp)

# Tkinter GUI を作成
root = tk.Tk()
root.title("会議アシスタント")
root.geometry("300x150")

exit_button = tk.Button(root, text="終了", command=stop_program)
exit_button.pack(pady=10)

generate_button = tk.Button(root, text="質問を生成", command=generate_questions)
generate_button.pack(pady=10)

# ループをバックグラウンドで実行
def run_task():
    global task_running
    while task_running:
        generate_questions()
        time.sleep(30)

threading.Thread(target=run_task, daemon=True).start()
root.mainloop()

print("Program exited.")
