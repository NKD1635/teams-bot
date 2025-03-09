"""
デモ用の入力待ちプログラム
文章3は「。」ごとに空白の入力待ちを挟みつつ表示し、input.txtに表示された分だけ書き込む。

"""
import time
import sys
import os

try:
    import msvcrt  # Windows
except ImportError:
    import termios
    import tty

def wait_for_space(prompt=""):
    print(prompt)
    while True:
        try:
            if os.name == 'nt':
                if msvcrt.getch() == b' ':
                    break
            else:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                    if ch == ' ':
                        break
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except KeyboardInterrupt:
            sys.exit(0)

def print_with_delay(text, delay=0.2):
    lines = text.strip().split('\n')
    for line in lines:
        print(line)
        time.sleep(delay)

def display_and_log_text(text, logfile='input.txt'):
    with open(logfile, 'w', encoding='utf-8') as f:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            f.write(char)
            f.flush()
            if char == '。':
                wait_for_space()
    #print("\n--- 文字起こし完了 ---")

text1 = '''
(log) Detecting microphone.
(log) Input level is adjusted.
(log) Decoding params beam=13 max-active=7000 lattice-beam=4
(log) Silence phones 1:2:3:4:5:6:7:8:9:10
(log) Removed 0 orphan nodes.
(log) Removing 0 orphan components.
(log) Noise cancellation is being set ...
準備が完了しました。'''

text2 = '音声認識を開始します'

text3 = '''本日は晴天なり。
音声認識テストを行います。
マイクの感度は良好です。
こちらの文章は実際の音声認識結果ではありません。
あくまでデモ用のダミーテキストです。'''

if __name__ == '__main__':
    # 文章1を表示（改行ごとに遅延）
    print_with_delay(text1)

    # 文章2表示後、スペースキー入力待機
    time.sleep(1)
    print(text2)
    wait_for_space()

    # 文章3表示（「。」ごとにスペースキー待機）、ログ記録
    #print("\n[文字起こし開始]\n")
    display_and_log_text(text3)

    # 終了処理
    #print("\n[終了するにはスペースキーを押してください]")
    wait_for_space()
    #print("プログラムを終了します。")
