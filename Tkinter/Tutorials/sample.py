"""
### プログラムの流れ

### 1. アプリケーションの準備 (`if __name__ == "__main__":` ブロック)

* `root = tk.Tk()`: Tkinterアプリケーションの土台となるメインウィンドウを作成する。
* `app = SimpleApp(root)`: 作成したメインウィンドウ (`root`) を使って、`SimpleApp` というアプリケーションのインスタンスを作成する。
* `root.mainloop()`: Tkinterアプリケーションを起動するコマンド。この行が実行されるとウィンドウが表示され、ユーザーのクリックやキー入力などのイベントを待ち受け、それに応じてプログラムが動作するようになる。

### 2. アプリケーションの初期設定 (`SimpleApp` クラスの `__init__` と `setup_app_window` メソッド)

* `SimpleApp` クラスが初期化される際（`__init__` メソッド内）に、`self.setup_app_window()` が呼び出される。
* `setup_app_window()` メソッドでは、メインウィンドウのタイトル（例: "Sample Tkinter App"）や初期サイズ（例: 400x300ピクセル）を設定する。

### 3. ウィジェットの作成と配置 (`create_widgets` メソッド)

* `create_widgets()` メソッドでは、ウィジェットを作成し、ウィンドウ内に配置する。
* ラベル: `tk.Label` でテキスト表示部分を作成し、`label.pack(pady=10)` でウィンドウの上部に10ピクセルの上下余白を付けて配置。
* エントリー: `tk.Entry` でユーザーがテキストを入力できる欄を作成し、`entry.pack(pady=5)` で5ピクセルの上下余白を付けて配置。このエントリーウィジェットは、後で入力内容を取得するために `self.entry_widget` として保存される。
* ボタン: `tk.Button` でクリックできるボタンを作成します。`command=self.handle_button_click` の部分で、「このボタンがクリックされたら、`self.handle_button_click` という関数を実行してください」と指示している。

### 4. ボタンのイベント処理 (`handle_button_click` メソッド)

* ユーザーが「入力内容を表示」ボタンをクリックすると、この `handle_button_click()` メソッドが自動的に呼び出される。
* メソッド内では、`self.entry_widget.get()` を使って、エントリー（入力欄）にユーザーが入力した現在のテキストを取得する。
* 最後に、`messagebox.showinfo()` を使って、取得したテキストをポップアップウィンドウとして画面に表示する。
"""

import tkinter as tk
from tkinter import messagebox

### メインアプリケーションのロジックを管理するクラス
class SimpleApp:
  def __init__(self, master):
    self.master = master
    self.entry_widget = None ### エントリーウィジェットを保持するための変数

    ### 1. アプリケーションの初期設定
    self.setup_app_window()

    ### 2. ウィジェットの作成と配置
    self.create_widgets()

  def setup_app_window(self):
    """
    ### アプリケーションのメインウィンドウを設定する。
    ### タイトルや初期サイズなどをここで定義する。
    """
    self.master.title("Sample Tkinter App")
    self.master.geometry("400x300")

  def create_widgets(self):
    """
    ### すべてのGUIウィジェット（ラベル、エントリー、ボタンなど）を作成し、
    ### ウィンドウ内に配置する。
    """
    ### ラベルの作成と配置
    label = tk.Label(self.master, text="何か入力してボタンを押してください:")
    label.pack(pady=10)

    ### エントリー（入力欄）の作成と配置
    self.entry_widget = tk.Entry(self.master, width=30) ### self.entry_widgetとして保存
    self.entry_widget.pack(pady=5)

    ### ボタンの作成と配置
    ### コマンドに、エントリーウィジェットを引数として渡す関数を指定する。
    button = tk.Button(self.master, text="入力内容を表示", command=self.handle_button_click)
    button.pack(pady=10)

    ### プログラムを終了するボタン
    exit_button = tk.Button(self.master, text="プログラムを終了", command=self.master.quit)
    exit_button.pack(pady=15)

  def handle_button_click(self):
    """
    ### ボタンがクリックされたときに実行されるイベントハンドラ。
    ### エントリーのテキストを取得し、メッセージボックスで表示する。
    """
    if self.entry_widget: ### エントリーウィジェットが存在するか確認
      input_text = self.entry_widget.get()
      messagebox.showinfo("入力内容", f"入力されたテキスト: {input_text}")
    else:
      messagebox.showerror("エラー", "エントリーウィジェットが見つかりません。")

### --- アプリケーションの実行 ---
if __name__ == "__main__":
  ### 1. Tkinterのルートウィンドウを初期化
  root = tk.Tk()

  ### 2. SimpleAppクラスのインスタンスを作成し、ウィンドウを渡す
  app = SimpleApp(root)

  ### 3. Tkinterイベントループを開始
  ### これにより、ウィンドウが表示され、ユーザーからの操作を待ち受ける。
  root.mainloop()

