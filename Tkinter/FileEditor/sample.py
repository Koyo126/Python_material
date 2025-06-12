import tkinter as tk
from tkinter import filedialog, messagebox

class FileEditorApp:
  """
  ### FileEditorAppクラスは、テキストファイルの読み込み、編集、保存機能を提供する。
  """
  def __init__(self, master):
    self.master = master
    self.current_filepath = None ### 現在開いているファイルのパスを保持する変数

    ### 1. アプリケーションの初期設定
    self.setup_app_window()

    ### 2. ウィジェットの作成と配置
    self.create_widgets()

  def setup_app_window(self):
    """
    ### アプリケーションのメインウィンドウを設定する。
    """
    self.master.title("シンプルファイルエディタ")
    self.master.geometry("600x500")

  def create_widgets(self):
    """
    ### GUIウィジェットを作成し、ウィンドウ内に配置する。
    """
    ### ファイル操作ボタンを配置するフレーム
    button_frame = tk.Frame(self.master)
    button_frame.pack(pady=5)

    ### ファイルを開くボタン
    open_button = tk.Button(button_frame, text="ファイルを開く", command=self.open_file)
    open_button.pack(side=tk.LEFT, padx=5) ### 左側に配置し、左右に5ピクセルの余白

    ### ファイルを保存するボタン
    save_button = tk.Button(button_frame, text="上書き保存", command=self.save_file)
    save_button.pack(side=tk.LEFT, padx=5)

    ### 名前を付けて保存するボタン
    save_as_button = tk.Button(button_frame, text="名前を付けて保存", command=self.save_file_as)
    save_as_button.pack(side=tk.LEFT, padx=5)

    ### プログラム終了ボタン
    exit_button = tk.Button(button_frame, text="終了", command=self.master.quit)
    exit_button.pack(side=tk.RIGHT, padx=5) ### 右側に配置

    ### テキスト編集エリア
    ### 複数行のテキストを入力・表示できるウィジェット
    ### wrap=tk.WORD で単語の途中で改行されないように設定
    self.text_area = tk.Text(self.master, wrap=tk.WORD)
    ### text_area をウィンドウの残りのスペースに合わせて拡大できるように設定
    self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

  def open_file(self):
    """
    ### ファイルダイアログを表示し、選択されたテキストファイルを読み込む。
    ### 読み込んだ内容はテキストエリアに表示される。
    """
    filepath = filedialog.askopenfilename(
      title="ファイルを開く",
      filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")]
    )
    if filepath:
      try:
        with open(filepath, "r", encoding="utf-8") as file:
          content = file.read()
        self.text_area.delete("1.0", tk.END) ### テキストエリアの既存内容をクリア
        self.text_area.insert("1.0", content) ### ファイル内容をテキストエリアに挿入
        self.current_filepath = filepath ### 現在開いているファイルのパスを更新
        self.master.title(f"シンプルファイルエディタ - {filepath}") ### ウィンドウタイトルを更新
      except Exception as e:
        messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました:\n{e}")

  def save_file(self):
    """
    ### 現在開いているファイルに、テキストエリアの内容を上書き保存する。
    ### まだファイルが開かれていない場合は、"名前を付けて保存"を呼び出す。
    """
    if self.current_filepath:
      try:
        with open(self.current_filepath, "w", encoding="utf-8") as file:
          file.write(self.text_area.get("1.0", tk.END)) ### テキストエリアの内容を書き込む
        messagebox.showinfo("保存完了", f"ファイルを上書き保存しました:\n{self.current_filepath}")
      except Exception as e:
        messagebox.showerror("エラー", f"ファイルの上書き保存に失敗しました:\n{e}")
    else:
      self.save_file_as() ### ファイルが開かれていない場合は名前を付けて保存

  def save_file_as(self):
    """
    ### "名前を付けて保存"ダイアログを表示し、テキストエリアの内容を保存する。
    ### 保存先のファイルパスを更新する。
    """
    filepath = filedialog.asksaveasfilename(
      title="ファイルを名前を付けて保存",
      defaultextension=".txt",
      filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")]
    )
    if filepath:
      try:
        with open(filepath, "w", encoding="utf-8") as file:
          file.write(self.text_area.get("1.0", tk.END))
        self.current_filepath = filepath ### 現在開いているファイルのパスを更新
        self.master.title(f"シンプルファイルエディタ - {filepath}") ### ウィンドウタイトルを更新
        messagebox.showinfo("保存完了", f"ファイルを保存しました:\n{self.current_filepath}")
      except Exception as e:
        messagebox.showerror("エラー", f"ファイルの保存に失敗しました:\n{e}")

### アプリケーションの開始点
if __name__ == "__main__":
  root = tk.Tk()
  app = FileEditorApp(root)
  root.mainloop()
