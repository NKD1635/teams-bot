import pyaudio
import json
from vosk import Model, KaldiRecognizer

def main():
    # Voskモデルのパスを指定（展開したモデルのディレクトリを指定してください）
    model_path = "model_japanese"  # 例: ダウンロードして展開した日本語モデルのフォルダ名
    model = Model("vosk-model-small-ja-0.22")
    
    # 認識器の初期化（サンプリングレートは16kHzが一般的）
    recognizer = KaldiRecognizer(model, 16000)
    
    # PyAudioの初期化とマイクからの音声キャプチャ設定
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)
    stream.start_stream()
    
    print("音声認識を開始しました。Ctrl+Cで終了します。")
    
    try:
        while True:
            # マイクからデータを読み込む（例：4000サンプルずつ）
            data = stream.read(4000, exception_on_overflow=False)
            # 十分なデータが溜まった場合、認識処理を実行
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print("認識結果:", text)
                    # 認識結果をinput.txtに追記
                    with open("input.txt", "a", encoding="utf-8") as f:
                        f.write(text + "\n")
            # partial_result を利用して部分認識結果を取得することも可能です
            # partial = json.loads(recognizer.PartialResult())
            # print("部分結果:", partial.get("partial", ""))
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
