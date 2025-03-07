import os
import time

def realtime_trim_file(filename, threshold, interval):
    """
    filename: 監視するファイル名
    threshold: しきい値（文字数）
    interval: 何秒ごとにファイルをチェックするか
    """
    while True:
        # 対象ファイルが存在するか確認
        if os.path.exists(filename):
            # ファイルを読み取り・書き込みモードで開く
            with open(filename, 'r+', encoding='utf-8') as f:
                content = f.read()
                if len(content) > threshold:
                    # 超えた分だけ先頭から削除
                    keep_content = content[-threshold:]
                    f.seek(0)
                    f.write(keep_content)
                    f.truncate()
        # interval 秒待ってから再度監視
        time.sleep(interval)

if __name__ == "__main__":
    realtime_trim_file("input.txt", threshold=50, interval=5)
  # 先頭からinput.txtの内容を消去する
  # threshold=50は文字数、50文字
  # interval=5は何秒おきで消去するか、5秒おき
