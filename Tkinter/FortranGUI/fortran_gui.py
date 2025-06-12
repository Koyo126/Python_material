import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import f90nml

class FortranNamelistApp:
  def __init__(self, root):
    ### メインウィンドウの設定
    self.root = root
    self.root.title("Fortran Namelist & Runner")
    #self.root.geometry("1000x875") ### ウィンドウサイズを設定

    ### フォントオブジェクトの定義 (デフォルト設定)
    self.default_font_family = 'Inter'
    self.default_font_size = 10
    self.bold_font_size = 12 ### グループタイトル用のサイズ

    self.label_font = tkfont.Font(family=self.default_font_family, size=self.default_font_size)
    self.button_font = tkfont.Font(family=self.default_font_family, size=self.default_font_size)
    self.entry_font = tkfont.Font(family=self.default_font_family, size=self.default_font_size)
    self.scrolledtext_font = tkfont.Font(family=self.default_font_family, size=self.default_font_size)
    self.group_title_font = tkfont.Font(family=self.default_font_family, size=self.bold_font_size, weight='bold')

    ### ユーザーが選択できるフォントファミリーのリスト
    self.available_font_families = ['Inter', 'Times New Roman', 'Arial', 'Courier New', 'Verdana']
    self.selected_font_family_var = tk.StringVar(value=self.default_font_family) ### デフォルトで選択されるフォント

    ### 現在のnamelistデータとファイルパス
    self.namelist_data = {}
    self.current_namelist_path = ""
    self.current_fortran_binary_path = ""

    ### UI要素のフレームを配置
    self.create_widgets()

  def create_widgets(self):
    ### --- Namelist ファイル操作フレーム ---
    file_frame = tk.LabelFrame(self.root, text="Namelist File Operations", padx=10, pady=10)
    file_frame.pack(pady=10, padx=10, fill="x")

    tk.Button(file_frame, text="Namelistファイルを読み込む", command=self.load_namelist, font=self.button_font).pack(side="left", padx=5)
    tk.Button(file_frame, text="Namelistファイルを保存", command=self.save_namelist, font=self.button_font).pack(side="left", padx=5)
    tk.Button(file_frame, text="Namelistファイルを新規作成", command=self.new_namelist, font=self.button_font).pack(side="left", padx=5)

    self.namelist_path_label = tk.Label(file_frame, text="ファイルパス: (未選択)", font=self.label_font)
    self.namelist_path_label.pack(side="right", padx=5)

    ### --- フォント選択フレーム ---
    font_selection_frame = tk.LabelFrame(self.root, text="Font Selection", padx=10, pady=5)
    font_selection_frame.pack(pady=5, padx=10, fill="x")

    tk.Label(font_selection_frame, text="フォントファミリー:", font=self.label_font).pack(side="left", padx=5)
    font_family_option_menu = tk.OptionMenu(font_selection_frame, self.selected_font_family_var, *self.available_font_families)
    font_family_option_menu.config(font=self.button_font) ### OptionMenu自体のフォントを設定
    font_family_option_menu.pack(side="left", padx=5)

    tk.Button(font_selection_frame, text="フォント適用", command=self.apply_selected_font, font=self.button_font).pack(side="left", padx=5)

    ### --- Namelist エディタフレーム ---
    self.editor_frame = tk.LabelFrame(self.root, text="Namelist Editor", padx=10, pady=10)
    self.editor_frame.pack(pady=10, padx=10, fill="both", expand=True)

    ### スクロール可能なフレームを作成
    self.editor_canvas = tk.Canvas(self.editor_frame)
    self.editor_canvas.pack(side="left", fill="both", expand=True)

    editor_scrollbar = tk.Scrollbar(self.editor_frame, orient="vertical", command=self.editor_canvas.yview)
    editor_scrollbar.pack(side="right", fill="y")
    self.editor_canvas.configure(yscrollcommand=editor_scrollbar.set)
    self.editor_canvas.bind('<Configure>', lambda e: self.editor_canvas.configure(scrollregion = self.editor_canvas.bbox("all")))

    self.namelist_inner_frame = tk.Frame(self.editor_canvas)
    self.editor_canvas.create_window((0, 0), window=self.namelist_inner_frame, anchor="nw")

    ### namelistエディタの入力ウィジェットを保持する辞書
    self.namelist_entry_widgets = {}

    ### --- 新しいエントリの追加フレーム ---
    self.add_entry_frame = tk.LabelFrame(self.root, text="新しいエントリの追加", padx=10, pady=10)
    self.add_entry_frame.pack(pady=10, padx=10, fill="x")

    ### 新しいグループの追加
    tk.Label(self.add_entry_frame, text="新しいグループ名:", font=self.label_font).pack(side="left", padx=5)
    self.new_group_name_entry = tk.Entry(self.add_entry_frame, width=20, font=self.entry_font)
    self.new_group_name_entry.pack(side="left", padx=5)
    tk.Button(self.add_entry_frame, text="グループを追加", command=self.add_new_group, font=self.button_font).pack(side="left", padx=5)

    ### 新しい変数の追加 (行を分ける)
    add_var_row_frame = tk.Frame(self.add_entry_frame)
    add_var_row_frame.pack(fill="x", pady=(10, 0))

    tk.Label(add_var_row_frame, text="グループに変数追加:", font=self.label_font).pack(side="left", padx=5)
    self.selected_group_var = tk.StringVar(self.root)
    self.group_selection_menu = tk.OptionMenu(add_var_row_frame, self.selected_group_var, "") ### 初期値は空
    self.group_selection_menu.config(font=self.button_font)
    self.group_selection_menu.pack(side="left", padx=5)
    
    tk.Label(add_var_row_frame, text="変数名:", font=self.label_font).pack(side="left", padx=5)
    self.new_var_name_entry = tk.Entry(add_var_row_frame, width=15, font=self.entry_font)
    self.new_var_name_entry.pack(side="left", padx=5)
    
    tk.Label(add_var_row_frame, text="値:", font=self.label_font).pack(side="left", padx=5)
    self.new_var_value_entry = tk.Entry(add_var_row_frame, width=20, font=self.entry_font)
    self.new_var_value_entry.pack(side="left", padx=5)
    
    tk.Button(add_var_row_frame, text="変数を追加", command=self.add_new_variable, font=self.button_font).pack(side="left", padx=5)


    ### --- Fortran バイナリ実行フレーム ---
    run_frame = tk.LabelFrame(self.root, text="Fortran Program Execution", padx=10, pady=10)
    run_frame.pack(pady=10, padx=10, fill="x")

    tk.Label(run_frame, text="Fortran バイナリパス:", font=self.label_font).pack(side="left", padx=5)
    self.binary_path_entry = tk.Entry(run_frame, width=40, font=self.entry_font)
    self.binary_path_entry.pack(side="left", padx=5, fill="x", expand=True)
    tk.Button(run_frame, text="参照", command=self.browse_binary, font=self.button_font).pack(side="left", padx=5)
    tk.Button(run_frame, text="実行", command=self.run_fortran_program, font=self.button_font).pack(side="left", padx=5)

    ### --- 実行結果表示フレーム ---
    output_frame = tk.LabelFrame(self.root, text="Program Output", padx=10, pady=10)
    output_frame.pack(pady=10, padx=10, fill="both", expand=True)

    self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10, font=self.scrolledtext_font)
    self.output_text.pack(fill="both", expand=True)
    self.output_text.config(state="disabled") ### ユーザーによる編集を禁止

    ### 初期状態でグループ選択メニューを更新
    self._update_group_selection_menu()

  def load_namelist(self):
    ### namelistファイルを読み込むダイアログを表示
    file_path = filedialog.askopenfilename(
      title="Namelistファイルを選択",
      filetypes=[("Namelist files", "*.nml"), ("All files", "*")]
    )
    if file_path:
      try:
        ### f90nmlでnamelistファイルを読み込み
        self.namelist_data = f90nml.read(file_path)
        self.current_namelist_path = file_path
        self.namelist_path_label.config(text=f"ファイルパス: {os.path.basename(file_path)}")
        self.populate_namelist_editor() ### GUIを更新
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Namelistファイル '{os.path.basename(file_path)}' を読み込みました。\n")
        self.output_text.config(state="disabled")
        self._update_group_selection_menu() ### グループ選択メニューも更新
      except Exception as e:
        messagebox.showerror("エラー", f"Namelistファイルの読み込みに失敗しました:\n{e}")

  def save_namelist(self):
    ### 現在namelistデータが読み込まれていない場合は、新規保存として処理
    if not self.namelist_data:
      self.save_namelist_as()
      return

    if not self.current_namelist_path:
      self.save_namelist_as()
      return

    ### 現在のGUIの値を内部データに反映
    self.update_namelist_data_from_gui()

    try:
      ### f90nmlでnamelistファイルを保存
      f90nml.write(self.namelist_data, self.current_namelist_path, force=True)
      #self.namelist_data.write(self.current_namelist_path, force=True)
      self.output_text.config(state="normal")
      self.output_text.delete(1.0, tk.END)
      self.output_text.insert(tk.END, f"Namelistファイル '{os.path.basename(self.current_namelist_path)}' を保存しました。\n")
      self.output_text.config(state="disabled")
    except Exception as e:
      messagebox.showerror("エラー", f"Namelistファイルの保存に失敗しました:\n{e}")

  def save_namelist_as(self):
    ### namelistファイルを新規保存するダイアログを表示
    file_path = filedialog.asksaveasfilename(
      title="Namelistファイルを保存",
      defaultextension=".nml",
      filetypes=[("Namelist files", "*.nml"), ("All files", "*")]
    )
    if file_path:
      ### 現在のGUIの値を内部データに反映
      self.update_namelist_data_from_gui()

      try:
        ### f90nmlでnamelistファイルを保存
        if not self.namelist_data:
          f90nml.write(self.namelist_data, file_path, force=True)
        else:
          f90nml.write(self.namelist_data, file_path, force=True)
          #self.namelist_data.write(file_path, force=True)
        self.current_namelist_path = file_path
        self.namelist_path_label.config(text=f"ファイルパス: {os.path.basename(file_path)}")
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Namelistファイル '{os.path.basename(file_path)}' を新規保存しました。\n")
        self.output_text.config(state="disabled")
      except Exception as e:
        messagebox.showerror("エラー", f"Namelistファイルの保存に失敗しました:\n{e}")

  def new_namelist(self):
    ### 新規namelistデータで初期化
    self.namelist_data = {}
    self.current_namelist_path = ""
    self.namelist_path_label.config(text="ファイルパス: (未選択)")
    self.populate_namelist_editor() ### GUIをクリア (空のデータで再描画)
    self.output_text.config(state="normal")
    self.output_text.delete(1.0, tk.END)
    self.output_text.insert(tk.END, "新しいnamelistデータを作成しました。下の「新しいエントリの追加」からグループや変数を追加してください。\n")
    self.output_text.config(state="disabled")
    self._update_group_selection_menu() ### グループ選択メニューも更新

  def populate_namelist_editor(self):
    ### 既存のウィジェットをクリア
    for widget in self.namelist_inner_frame.winfo_children():
      widget.destroy()
    self.namelist_entry_widgets = {}

    ### namelistデータが空の場合
    if not self.namelist_data:
      tk.Label(self.namelist_inner_frame, text="Namelistデータがありません。下の「新しいエントリの追加」からグループを追加してください。", font=self.label_font).pack(pady=10)
      return ### ここはメッセージ表示のみで、新しいエントリ追加機能は別途提供

    ### 各グループと変数を表示
    for group_name, variables in self.namelist_data.items():
      ### グループ名を表示
      tk.Label(self.namelist_inner_frame, text=f"&{group_name.upper()}", font=self.group_title_font).pack(anchor="w", pady=(10, 0))
      
      ### 各変数を表示
      for var_name, value in variables.items():
        row_frame = tk.Frame(self.namelist_inner_frame)
        row_frame.pack(fill="x", padx=10, pady=2)

        tk.Label(row_frame, text=f"{var_name.lower()} =", width=15, anchor="w", font=self.label_font).pack(side="left")
        
        ### 値を文字列として表示
        ### 配列はカンマ区切りで表示 (f90nmlは配列をリストとして扱うため)
        display_value = ', '.join(map(str, value)) if isinstance(value, list) else str(value)
        
        entry_var = tk.StringVar(value=display_value)
        entry = tk.Entry(row_frame, textvariable=entry_var, width=50, font=self.entry_font)
        entry.pack(side="left", fill="x", expand=True)

        ### 後で値を読み取るためにウィジェットを保存
        self.namelist_entry_widgets[(group_name, var_name)] = entry_var
      
      ### グループの終わり
      tk.Label(self.namelist_inner_frame, text="/", font=self.group_title_font).pack(anchor="w", pady=(0, 5))

    ### スクロール領域を更新
    self.namelist_inner_frame.update_idletasks()
    self.editor_canvas.config(scrollregion=self.editor_canvas.bbox("all"))

  def update_namelist_data_from_gui(self):
    """GUIの入力ウィジェットから現在のnamelist_dataを更新します。"""
    ### GUIの値を内部のnamelistデータに反映
    for (group_name, var_name), entry_var in self.namelist_entry_widgets.items():
      raw_value = entry_var.get()

      ### _convert_string_to_fortran_type ヘルパー関数を使って値を型変換
      converted_value = self._convert_string_to_fortran_type(raw_value)

      ### 内部データ (self.namelist_data) を更新
      ### group_name が存在しない場合は新しい辞書を作成
      if group_name not in self.namelist_data:
        self.namelist_data[group_name] = {}

      self.namelist_data[group_name][var_name] = converted_value

### 新しいヘルパー関数を追加
  def _convert_string_to_fortran_type(self, value_str):
    ### Fortranのデータ型に合うように文字列の変換を試みるヘルパー関数
    value_str = value_str.strip() ### 前後の空白を削除

    ### 空文字列の場合
    if not value_str:
      return "" ### あるいはNone, デフォルト値など、namelistの仕様による

    ### 配列の可能性 (カンマ区切り)
    if ',' in value_str:
      elements = [elem.strip() for elem in value_str.split(',')]
      converted_elements = []
      for elem in elements:
        converted_elements.append(self._convert_single_value_to_fortran_type(elem))
      return converted_elements
    else: ### 単一値の可能性
      return self._convert_single_value_to_fortran_type(value_str)

  def _convert_single_value_to_fortran_type(self, s):
    ### 単一の文字列値をFortranのデータ型に変換するヘルパー関数
    s_lower = s.lower()

    ### 真偽値
    if s_lower == '.true.' or s_lower == 'true' or s_lower == 't':
      return True
    elif s_lower == '.false.' or s_lower == 'false' or s_lower == 'f':
      return False

    ### 数値（整数または浮動小数点数）
    try:
      if '.' in s or 'e' in s_lower or 'd' in s_lower: ### 小数点や指数表記があればfloat
        return float(s.replace('d', 'e')) ### FortranのD表記をPythonのe表記に変換
      else:
        return int(s)
    except ValueError:
      pass ### 数値変換に失敗したら、そのまま文字列として扱う

    ### それ以外は文字列として返す (f90nmlは自動的にクォートを処理)
    return s

  def add_new_group(self):
    new_group_name = self.new_group_name_entry.get().strip().upper() ### 大文字に変換

    if not new_group_name:
      messagebox.showerror("エラー", "新しいグループ名を入力してください。")
      return

    if new_group_name in self.namelist_data:
      messagebox.showwarning("警告", f"グループ '{new_group_name}' は既に存在します。")
      return

    self.namelist_data[new_group_name] = {} ### 新しい空のグループを追加
    self.populate_namelist_editor() ### エディタを更新
    self._update_group_selection_menu() ### グループ選択メニューを更新
    self.new_group_name_entry.delete(0, tk.END) ### 入力欄をクリア
    messagebox.showinfo("成功", f"グループ '{new_group_name}' を追加しました。")

  def add_new_variable(self):
    selected_group = self.selected_group_var.get()
    new_var_name = self.new_var_name_entry.get().strip().lower() ### 小文字に変換
    new_var_value_str = self.new_var_value_entry.get().strip()

    if not selected_group:
      messagebox.showerror("エラー", "変数追加先のグループを選択してください。")
      return
    if not new_var_name:
      messagebox.showerror("エラー", "新しい変数名を入力してください。")
      return
    ### 値は空でも許容するが、警告は出す
    if not new_var_value_str:
      response = messagebox.askyesno("警告", "変数の値が空です。このまま追加しますか？")
      if not response:
        return

    if new_var_name in self.namelist_data.get(selected_group, {}):
      messagebox.showwarning("警告", f"グループ '{selected_group}' 内に変数 '{new_var_name}' は既に存在します。")
      return

    ### 値の型を推測して変換
    converted_value = self._convert_value_for_fortran(new_var_value_str)

    if selected_group not in self.namelist_data:
      self.namelist_data[selected_group] = {} ### 念のためグループが存在しない場合に作成

    self.namelist_data[selected_group][new_var_name] = converted_value
    self.populate_namelist_editor() ### エディタを更新
    self.new_var_name_entry.delete(0, tk.END) ### 入力欄をクリア
    self.new_var_value_entry.delete(0, tk.END) ### 入力欄をクリア
    messagebox.showinfo("成功", f"グループ '{selected_group}' に変数 '{new_var_name}' を追加しました。")

  def _convert_value_for_fortran(self, value_str):
    """Fortranのデータ型に合うように文字列の変換を試みるヘルパー関数"""
    if ',' in value_str: ### 配列の可能性
      elements = [elem.strip() for elem in value_str.split(',')]
      converted_elements = []
      for elem in elements:
        try:
          if '.' in elem:
            converted_elements.append(float(elem))
          else:
            converted_elements.append(int(elem))
        except ValueError:
          converted_elements.append(elem) ### 変換できなければ文字列
      return converted_elements
    else: ### 単一値の可能性
      try:
        if '.' in value_str:
          return float(value_str)
        else:
          return int(value_str)
      except ValueError:
        if value_str.lower() == '.true.' or value_str.lower() == 'true':
          return True
        elif value_str.lower() == '.false.' or value_str.lower() == 'false':
          return False
        return value_str ### 変換できなければ文字列

  def _update_group_selection_menu(self):
    """グループ選択メニューのオプションを更新するヘルパー関数"""
    menu = self.group_selection_menu["menu"]
    menu.delete(0, "end") ### 現在のオプションをすべて削除
    
    group_names = sorted(list(self.namelist_data.keys()))
    if not group_names:
      self.selected_group_var.set("") ### グループがない場合は選択をクリア
      menu.add_command(label="(グループがありません)", state="disabled")
    else:
      ### 現在選択されているグループがリストにない場合は、最初のグループを選択する
      if self.selected_group_var.get() not in group_names:
        self.selected_group_var.set(group_names[0])

      for group_name in group_names:
        menu.add_command(label=group_name, command=lambda g=group_name: self.selected_group_var.set(g), font=self.label_font)
      
      ### 最初のグループをデフォルトで選択状態にする（もし存在すれば）
      if group_names and not self.selected_group_var.get():
        self.selected_group_var.set(group_names[0])


  def browse_binary(self):
    ### Fortranバイナリのパスを選択
    file_path = filedialog.askopenfilename(
      title="Fortran実行バイナリを選択",
      filetypes=[("Executable files", "*")]
    )
    if file_path:
      self.binary_path_entry.delete(0, tk.END)
      self.binary_path_entry.insert(0, file_path)
      self.current_fortran_binary_path = file_path

  def run_fortran_program(self):
    binary_path = self.binary_path_entry.get()

    if not binary_path:
      messagebox.showerror("エラー", "Fortranバイナリのパスが指定されていません。")
      return
    if not os.path.exists(binary_path):
      messagebox.showerror("エラー", "指定されたFortranバイナリが存在しません。")
      return
    if not os.access(binary_path, os.X_OK):
      messagebox.showerror("エラー", "指定されたFortranバイナリは実行権限がありません。")
      return

    ### 実行結果表示エリアをクリア
    self.output_text.config(state="normal")
    self.output_text.delete(1.0, tk.END)
    self.output_text.insert(tk.END, f"Fortranプログラム '{os.path.basename(binary_path)}' を実行中...\n\n")
    self.output_text.config(state="disabled")

    try:
      ### サブプロセスとしてFortranプログラムを実行
      ### 現在のnamelistファイルのディレクトリを作業ディレクトリとする
      working_dir = os.path.dirname(self.current_namelist_path) if self.current_namelist_path else os.getcwd()
      
      process = subprocess.Popen(
        [binary_path],
        cwd=working_dir, ### 作業ディレクトリを設定
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True, ### テキストモードで出力を扱う
        encoding='utf-8' ### エンコーディングを指定
      )
      stdout, stderr = process.communicate() ### プログラムの終了を待つ

      ### 標準出力と標準エラー出力を表示
      self.output_text.config(state="normal")
      if stdout:
        self.output_text.insert(tk.END, "--- 標準出力 ---\n")
        self.output_text.insert(tk.END, stdout)
      if stderr:
        self.output_text.insert(tk.END, "\n--- 標準エラー出力 ---\n")
        self.output_text.insert(tk.END, stderr)
      
      if process.returncode == 0:
        self.output_text.insert(tk.END, "\nプログラムは正常に終了しました。\n")
      else:
        self.output_text.insert(tk.END, f"\nプログラムはエラー終了しました。終了コード: {process.returncode}\n")
      self.output_text.config(state="disabled")

    except Exception as e:
      self.output_text.config(state="normal")
      self.output_text.insert(tk.END, f"\nFortranプログラムの実行中にエラーが発生しました:\n{e}\n")
      self.output_text.config(state="disabled")
      messagebox.showerror("実行エラー", f"Fortranプログラムの実行中にエラーが発生しました:\n{e}")

  def apply_selected_font(self):
    ### ドロップダウンで選択されたフォントファミリーを取得
    new_font_family = self.selected_font_family_var.get()
    
    ### 各フォントオブジェクトのファミリーを更新
    self.label_font.config(family=new_font_family)
    self.button_font.config(family=new_font_family)
    self.entry_font.config(family=new_font_family)
    self.scrolledtext_font.config(family=new_font_family)
    self.group_title_font.config(family=new_font_family)

    ### すべてのウィジェットのフォントを再適用 (既存ウィジェット向け)
    self._update_all_widget_fonts(self.root)
    
    ### Namelistエディタの内容を再描画して、動的に生成される入力欄も更新されるようにする
    self.populate_namelist_editor()
    
    messagebox.showinfo("フォント変更", f"フォントを '{new_font_family}' に変更しました。")

  def _update_all_widget_fonts(self, parent_widget):
    """
    再帰的にすべてのウィジェットのフォントを更新する。
    ウィジェットタイプに基づいて定義済みのフォントオブジェクトを適用する。
    """
    for child in parent_widget.winfo_children():
      try:
        if isinstance(child, tk.Label):
          ### LabelFrameのタイトルはLabelではないため、個別の処理は不要
          child.config(font=self.label_font)
        elif isinstance(child, tk.Button):
          child.config(font=self.button_font)
        elif isinstance(child, tk.Entry):
          child.config(font=self.entry_font)
        elif isinstance(child, scrolledtext.ScrolledText):
          child.config(font=self.scrolledtext_font)
        elif isinstance(child, tk.OptionMenu):
          ### OptionMenu自体はButtonウィジェットのように振る舞う
          child.config(font=self.button_font)
          ### OptionMenuの内部メニューのフォントも更新 (より詳細な制御が必要な場合)
          ### 通常、Tkinterのデフォルト設定で十分だが、必要であれば
          ### 例えば、tk.option_add('*Menu.font', self.label_font) のように設定できるが、
          ### 実行中のメニューには適用されない可能性がある。
          pass
        elif isinstance(child, tk.LabelFrame):
          ### LabelFrameのタイトルは、tkfont.Fontオブジェクトで直接更新できないため、
          ### ここでは何もしません。内部のウィジェットには再帰的に適用される。
          pass

        ### 再帰的に子ウィジェットのフォントも更新
        self._update_all_widget_fonts(child)
      except tk.TclError:
        ### 'font' オプションを持たないウィジェットがある場合のエラーを無視
        pass

### アプリケーションの実行
if __name__ == "__main__":
  root = tk.Tk()
  app = FortranNamelistApp(root)
  root.mainloop()

