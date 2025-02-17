from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QFrame, QTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QTimer
import sys

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Web Browser")
        self.setGeometry(100, 100, 1024, 768)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://teams.microsoft.com"))

        self.url_bar = QLineEdit()
        self.url_bar.setText("https://teams.microsoft.com")
        self.url_bar.returnPressed.connect(self.load_url)

        self.go_button = QPushButton("移動")
        self.go_button.clicked.connect(self.load_url)

        # 右側の余白スペース（output.txtを表示）
        self.right_space = QTextEdit()
        self.right_space.setFixedWidth(300)  # 余白の幅を設定
        self.right_space.setReadOnly(True)
        self.update_output_text()

        # 1秒ごとにoutput.txtを更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_output_text)
        self.timer.start(1000)

        # メインのレイアウト（横方向）
        main_layout = QHBoxLayout()

        # 左側のレイアウト（URLバー、ボタン、Webビュー）
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.url_bar)
        left_layout.addWidget(self.go_button)
        left_layout.addWidget(self.browser)

        # レイアウトを追加
        container = QWidget()
        container.setLayout(left_layout)
        main_layout.addWidget(container)
        main_layout.addWidget(self.right_space)  # 右側の余白（output.txt表示）

        main_container = QWidget()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

    def load_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))  # ✅ 文字列を QUrl に変換

    def update_output_text(self):
        try:
            with open("output.txt", "r", encoding="utf-8") as file:
                self.right_space.setText(file.read())
        except FileNotFoundError:
            self.right_space.setText("output.txt not found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
