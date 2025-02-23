#ダミーの会話を生成し、input.txtに書き込むスクリプト

import time
import random
import threading
import sys

# 話題リスト (トピックを示すフレーズ)
FAKE_TOPICS = [
    "今からプログラムの実装方法を決めていきましょう。",
    "インドネシアの出張の件なんだけど、",
    "次のリリース計画を詰めたいのですが、",
    "新しいデザインコンセプトについて話し合いましょう。",
    "顧客からのフィードバックが届いたので共有しますね。"
]

# 会議文言リスト (具体的な発言やコメント)
FAKE_MEETING_LINES = [
    "それは前回の要件定義をベースに進められそうです。",
    "どう思いますか？",
    "確認事項がいくつかありそうですね。",
    "わからない部分があるので、一度洗い出しましょう。",
    "次のテーマへ移る準備はできていますか？",
    "今日中に対応の方向性を決めたいところです。",
    "その点は○○さんに相談してから最終決定しましょう。",
    "優先度としては低めだと思いますが、念のため議論しましょう。",
    "実装コストの見積もりを早めに出す必要があります。",
    "納期的に厳しい場合、スコープ調整も考えないといけません。"
]

INPUT_FILE = "input.txt"
running = True

def mock_meeting_loop():
    """
    10 秒ごとにランダムに「話題 + 会議文言」を 1 行生成し、
    input.txt を空にしてから新しい行を書き込むループ。
    """
    global running

    while running:
        topic = random.choice(FAKE_TOPICS)
        line = random.choice(FAKE_MEETING_LINES)

        # 組み合わせた新しい 1 行
        new_line = f"{topic} {line}"

        # 1) ファイルを空にする（ 'w' モードで何も書かず即クローズ）
        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            pass  # ここで一旦中身を空に

        # 2) 改めて追記モード('a')で新_line を書き込む
        with open(INPUT_FILE, "a", encoding="utf-8") as f:
            f.write(new_line + "\n")

        print(f"[MockMeeting] Generated line: {new_line}")

        # 10 秒スリープ
        time.sleep(10)

def start_mock_meeting():
    """モック会議の生成を開始する関数"""
    meeting_thread = threading.Thread(target=mock_meeting_loop, daemon=True)
    meeting_thread.start()
    return meeting_thread

def stop_mock_meeting():
    """モック会議のループを停止"""
    global running
    running = False

if __name__ == "__main__":
    print("Mock meeting generator started. Press Ctrl+C to stop.")
    start_mock_meeting()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping mock meeting...")
        stop_mock_meeting()
        sys.exit(0)
