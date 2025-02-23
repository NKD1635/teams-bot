# リアルタイムで質問生成できるようにする。
# LLM送信判定基準
# 以下を満たす場合送信する。満たさない場合は送信しない。3秒おきで判定する。
# 1. キーワードが含まれている場合
# 2. 前回のテキストと大きく異なる場合(5単語以上の差分がある場合)



import google.generativeai as genai
import time
import threading
import tkinter as tk

# -- ① Geminiの設定 --
genai.configure(api_key="xxxxxx")  # GeminiのAPIキーを取得して設定

# システムロールの指示はそのまま
system_content = """あなたは私のAIアシスタントです。あなたは会議の他に以下のスキルを備えています。

# 会議時の質問提示スキル
* 会議中の会話をインプットすると、3つの質問とその質問の意図を生成します。
"""
# messagesは現状未使用だが、残しておく
messages = [{"role": "system", "content": system_content}]

# -- ② 質問生成用スキル（既存） --
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


# -- ③ 入出力ファイル確認・作成 --
def ensure_file_exists(filepath: str, initial_content: str = ""):
    try:
        with open(filepath, "x", encoding="utf-8") as file:
            file.write(initial_content)
    except FileExistsError:
        pass

def read_input_file(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        ensure_file_exists(filepath)
        return ""

def write_output_file(filepath: str, content: str):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

input_file = "input.txt"
output_file = "output.txt"
ensure_file_exists(input_file)
ensure_file_exists(output_file)

# -- ④ 文脈切り替え検知＆キーワードトリガーを行う関数を追加 --
# ここでは非常に簡易的な例として、「前回のテキストと大きく異なる」または
# 特定キーワードが含まれる場合にTrueを返す。
import re

KEYWORDS = ["わからない", "確認", "どう思う", "次のテーマ", "決定", "相談", "議論", "見積もり", "納期", "スコープ"]

def detect_trigger(new_text: str, old_text: str) -> bool:
    # 空の場合は無視
    if not new_text:
        print("テキストが空です")
        return False
    
    # 前回と同一なら何もしない
    if new_text == old_text:
        print("前回と同じテキストです")
        return False

    # キーワードトリガー検出
    for kw in KEYWORDS:
        if kw in new_text:
            print(f"キーワード '{kw}' が含まれています")
            return True

    # 文脈切り替わり（超簡易版）：前回と似ていない度合いを判定
    # ここでは単語セットを比較し、ある程度差分が多ければトピック変更とみなす
    new_words = set(new_text.split())
    old_words = set(old_text.split())
    diff = new_words.symmetric_difference(old_words)
    # 差分の単語数が一定以上あればトリガーとみなす（適宜閾値調整）
    if len(diff) > 5:   # 5単語以上の差分がある場合
        print("文脈が大きく変わりました")
        return True

    return False

# -- ⑤ 前回のテキストを保持する変数を用意 --
last_text = ""


# -- ⑥ メインの質問生成関数を修正 --
def generate_questions():
    global last_text
    text = read_input_file(input_file)

    # トリガー判定
    if detect_trigger(text, last_text):
        # 質問生成を実行
        intent = "generate_meeting_questions"
        skill = skills[intent]
        resp = skill(meeting_text=text)
        #print(f"bot> {resp}")
        print("bot>質問が生成されました。")
        write_output_file(output_file, resp)
    
    # 最後に last_text を更新
    last_text = text


# -- ⑦ Tkinter GUI (最小限修正) --
task_running = True

def stop_program():
    global task_running
    task_running = False
    root.quit()

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
        time.sleep(3)  # ここは変えず、3秒ごとにチェックだけ行う
                        # トリガーに該当しなければLLM呼び出しはしない
        print("LLM送信するか判定中...")
root_thread = threading.Thread(target=run_task, daemon=True)
root_thread.start()

root.mainloop()
print("プログラムが終了しました。")
