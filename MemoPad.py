# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk

import configparser as cp
import os

import subwindow as sw
import dbmodule as db

# アプリ定数
TITLE = 'task_manager'
CONFIGNAME = 'config/config.ini'
ROOT_WIDTH = 800
ROOT_HEIGHT = 480

F_SIZE = {'L':20, 'M':15, 'S':10}   # 文字サイズ


# ---------------------------------------------------------------------------
# メインフレーム(アプリ本体)
# ---------------------------------------------------------------------------
class MemoPad(tk.Frame):
    # コンストラクタ
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH)
        self.font = 'メイリオ'    # 使用フォント
        self.charset = 'utf-8'  # 使用文字コード(ただし，iniファイルは常時UTF-8)
        self.edit_flag = False  # 編集状態時の移動制限
        db.create_database()  # (ない場合)DB初期生成
        self.menu_create()
        self.home()
    # ---------------------------------------------------------------------------
    # フレーム生成
    #
    # アプリ本体で動作する大枠を生成．
    # ---------------------------------------------------------------------------
    # メニューバー生成
    # ---------------------------------------------------------------------------
    def menu_create(self):
        
        # 既に存在している場合はメニューを破棄して再生成
        try:
            self.menu_frame.destroy()
        except:
            pass

    # ---------------------------------------------------------------------------
    # メインフレーム生成
    # ---------------------------------------------------------------------------
    def main_create(self, w, h):
        
        # 既に存在している場合はメインフレームを破棄して再生成
        try:
            self.main_frame.destroy()
        except:
            pass
        self.main_frame = tk.Frame(self, width=w, height=h)
        self.main_frame.pack(anchor=tk.CENTER, side=tk.TOP, padx=5, pady=5, fill=tk.BOTH)
    
    # ---------------------------------------------------------------------------
    # 画面遷移
    # 
    # 各画面ごとの処理を記載．
    # ---------------------------------------------------------------------------
    # ホーム画面 
    # ---------------------------------------------------------------------------
    def home(self):
        # 編集画面へ
        def submit_update(event):
            # ok
            def submit_ok(event):
                sub_win.destroy()
            
            # 項目指定確認
            if self.main_tree.focus().isdigit():
                memo = db.select_memo_one(self.main_tree.focus())
                self.update_memo(memo[0])
            else:
                # サブウィンドウ
                sub_win = sw.SubWindow('エラー', '編集項目を指定してください', self.font)
                ok_button = tk.Button(sub_win.frame, text='OK', width=8, font=(self.font, F_SIZE['S']))
                ok_button.bind('<1>', submit_ok)
                ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 登録してサブウィンドウを表示
        def submit_newcreate(event):
            self.insert_memo()
        
        # 削除
        def submit_delete(event):
            # はい(データを削除して戻る)
            def submit_yes(event):
                # ok
                def submit_ok(event):
                    sub_sub_win.destroy()
                db.delete_memo(self.main_tree.focus())
                self.home()
                sub_win.destroy()
                sub_sub_win = sw.SubWindow('削除成功', '削除しました！', self.font)
                ok_button = tk.Button(sub_sub_win.frame, text='OK', width=8, font=(self.font, F_SIZE['S']))
                ok_button.bind('<1>', submit_ok)
                ok_button.pack(side=tk.LEFT, padx=5, pady=5)
            
            # いいえ
            def submit_no(event):
                sub_win.destroy()
            
            # ok
            def submit_ok(event):
                sub_win.destroy()
            
            # 項目を指定している場合のみ削除確認
            if self.main_tree.focus().isdigit():
                # Yes/Noウィンドウ
                sub_win = sw.SubWindow('削除確認', '削除しますか？', self.font)
                # はいボタン
                yes_button = tk.Button(sub_win.frame, text='はい', width=8, font=(self.font, F_SIZE['S']))
                yes_button.bind('<1>', submit_yes)
                yes_button.pack(side=tk.LEFT, padx=5, pady=5)
                # いいえボタン
                no_button = tk.Button(sub_win.frame, text='いいえ', width=8, font=(self.font, F_SIZE['S']))
                no_button.bind('<1>', submit_no)
                no_button.pack(side=tk.LEFT, padx=5, pady=5)
            else:
                # サブウィンドウ
                sub_win = sw.SubWindow('エラー', '削除する項目を指定してください', self.font)
                ok_button = tk.Button(sub_win.frame, text='OK', width=8, font=(self.font, F_SIZE['S']))
                ok_button.bind('<1>', submit_ok)
                ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 編集中フラグ設定
        self.edit_flag = False

        # 機能ラベル
        self.main_create(ROOT_WIDTH, ROOT_HEIGHT)
        self.label_menuname = tk.Label(self.main_frame, text='タスク一覧', width=15, font=(self.font, F_SIZE['L']))
        self.label_menuname.pack(padx=5, pady=15)
        
        # ツリービュー
        self.tree_frame = tk.Frame(self.main_frame)
        self.tree_frame.pack()
        self.main_tree = ttk.Treeview(self.tree_frame, padding=5, height=12)
        self.main_tree["columns"] = (1, 2)
        self.main_tree["show"] = 'headings'
        self.main_tree.column(1, width=100)
        self.main_tree.column(2, width=400)
        self.main_tree.heading(1, text="タイトル")
        self.main_tree.heading(2, text="本文(抜粋)")
        self.main_tree_style = ttk.Style()
        self.main_tree_style.configure("Treeview", font=(self.font, F_SIZE['S']))
        self.main_tree_style.configure("Treeview.Heading", font=(self.font, F_SIZE['M'], tk.font.BOLD))
        
        # ツリースクロール
        self.main_scroll = tk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.main_tree.yview)
        self.main_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_tree['yscrollcommand'] = self.main_scroll.set
        
        # アイテムの取得＆挿入
        # SQLからアイテム取得
        for i in db.select_memo():
            print(i)
            text = i[2].replace('\n', ' ')
            self.main_tree.insert('', tk.END, iid=i[0], values=(i[1], text[0:30]))
        self.main_tree.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 出力/編集/削除
        self.edit_frame = tk.Frame(self.main_frame)
        self.edit_frame.pack(padx=5, pady=5)
        self.button_update = tk.Button(self.edit_frame, text='編集', width=8, font=(self.font, F_SIZE['S']))
        self.button_update.bind('<1>', submit_update)
        self.button_update.pack(side=tk.LEFT, padx=15, pady=5)
        self.button_delete = tk.Button(self.edit_frame, text='削除', width=8, font=(self.font, F_SIZE['S']))
        self.button_delete.bind('<1>', submit_delete)
        self.button_delete.pack(side=tk.LEFT, padx=15, pady=5)
        self.button_create = tk.Button(self.edit_frame, text='新規作成', width=8, font=(self.font, F_SIZE['S']))
        self.button_create.bind('<1>', submit_newcreate)
        self.button_create.pack(side=tk.LEFT, padx=15, pady=5)
        print(self.main_tree.focus())
    
    # ---------------------------------------------------------------------------
    # 登録画面
    # ---------------------------------------------------------------------------
    def insert_memo(self):
        
        # 登録してサブウィンドウを表示
        def submit_create(event):
            def submit_ok(event):
                sub_win.destroy()
                self.home()
            
            title = str(self.memo_title.get())
            # タイトルが1文字以上20文字以下の場合のみ登録処理
            if len(title) < 1 :
                sub_win = sw.SubWindow('登録失敗', 'タイトルを入力してください', self.font)
            elif len(title) > 20:
                sub_win = sw.SubWindow('登録失敗', 'タイトルは20文字以下で指定してください', self.font)
            else:
                memo = [title, self.memo_input.get('1.0', tk.END)]
                db.insert_memo(memo)
                # サブウィンドウ
                sub_win = sw.SubWindow('登録完了', 'メモを登録しました！', self.font)
            ok_button = tk.Button(sub_win.frame, text='OK', width=8, font=(self.font, F_SIZE['S']))
            ok_button.bind('<1>', submit_ok)
            ok_button.pack(side=tk.LEFT, padx=5, pady=5)

        # 戻る
        def submit_return(event):
            self.home()
        
        # 編集中フラグ設定
        self.edit_flag = True

        # 機能ラベル
        self.main_create(ROOT_WIDTH, ROOT_HEIGHT)
        self.label_menuname = tk.Label(self.main_frame, text='新規作成', width=15, font=(self.font, F_SIZE['L']))
        self.label_menuname.pack(padx=5, pady=5)
        self.make_memo_frame()
        
        self.edit_frame = tk.Frame(self.main_frame)
        self.edit_frame.pack(padx=15, pady=5)

        # 登録ボタン
        self.submit_create = tk.Button(self.main_frame, text='登録', width=8, font=(self.font, F_SIZE['S']))
        self.submit_create.bind('<1>', submit_create)
        self.submit_create.pack(side=tk.RIGHT, padx=15, pady=15)

        # 戻るボタン
        self.submit_return = tk.Button(self.main_frame, text='戻る', width=8, font=(self.font, F_SIZE['S']))
        self.submit_return.bind('<1>', submit_return)
        self.submit_return.pack(side=tk.RIGHT, padx=15, pady=15)

    # ---------------------------------------------------------------------------
    # 編集画面 
    # ---------------------------------------------------------------------------
    def update_memo(self, memo):
        
        # 登録してサブウィンドウを表示
        def submit_update(event):
            def submit_ok(event):
                sub_win.destroy()
                self.home()
        
            title = str(self.memo_title.get())
            # タイトルが1文字以上20文字以下の場合のみ登録処理
            if len(title) < 1 :
                sub_win = sw.SubWindow('更新失敗', 'タイトルを入力してください', self.font)
            elif len(title) > 20:
                sub_win = sw.SubWindow('更新失敗', 'タイトルは20文字以下で指定してください', self.font)
            else:
                update = [title, self.memo_input.get('1.0', tk.END), memo[0]]
                db.update_memo(update)
                sub_win = sw.SubWindow('更新完了', 'メモを更新しました！', self.font)
            ok_button = tk.Button(sub_win.frame, text='OK', width=8, font=(self.font, F_SIZE['S']))
            ok_button.bind('<1>', submit_ok)
            ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 編集中フラグ設定
        self.edit_flag = True

        # 機能ラベル
        self.main_create(ROOT_WIDTH, ROOT_HEIGHT)
        self.label_menuname = tk.Label(self.main_frame, text='メモ編集', width=15, font=(self.font, F_SIZE['L']))
        self.label_menuname.pack(padx=5, pady=15)
        self.make_memo_frame()
        self.memo_title.insert(tk.END, memo[1])
        self.memo_input.insert(tk.END, memo[2])
        
        # 登録ボタン
        self.submit_update = tk.Button(self.main_frame, text='更新', width=15, font=(self.font, F_SIZE['S']))
        self.submit_update.bind('<1>', submit_update)
        self.submit_update.pack(padx=5, pady=15)

    # ---------------------------------------------------------------------------
    # メモ枠組 
    # ---------------------------------------------------------------------------
    def make_memo_frame(self):
        
        # タイトル
        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.pack(padx=45, pady=15, fill=tk.BOTH)
        self.label_memo_title = tk.Label(self.title_frame, text='タイトル(1～20文字)', font=(self.font, F_SIZE['S']))
        self.label_memo_title.pack(side=tk.LEFT, fill=tk.X, padx=5)
        self.memo_title = tk.Entry(self.title_frame, font=(self.font, F_SIZE['S']))
        self.memo_title.pack(side=tk.LEFT, fill=tk.X, padx=5)
        
        # 本文
        self.memo_frame = tk.Frame(self.main_frame)
        self.memo_frame.pack()
        self.memo_input = tk.Text(self.memo_frame, height=10, font=(self.font, F_SIZE['S']))
        
        # 本文スクロール
        self.memo_scroll = tk.Scrollbar(self.memo_frame, orient=tk.VERTICAL, command=self.memo_input.yview)
        self.memo_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.memo_input['yscrollcommand'] = self.memo_scroll.set
        self.memo_input.pack()

        # チェックボックス
        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.pack(padx=40, pady=5, fill=tk.BOTH)
        self.label_memo_title = tk.Label(self.title_frame, text='リマインドする', font=(self.font, F_SIZE['S']))
        self.label_memo_title.pack(side=tk.LEFT, fill=tk.X, padx=5)
        self.memo_title = tk.Checkbutton(self.title_frame)
        self.memo_title.pack(side=tk.LEFT, fill=tk.X, padx=5)

        # メアド
        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.pack(padx=40, pady=5, fill=tk.BOTH)
        self.label_memo_title = tk.Label(self.title_frame, text='メールアドレス', font=(self.font, F_SIZE['S']))
        self.label_memo_title.pack(side=tk.LEFT, fill=tk.X, padx=5)
        self.memo_title = tk.Entry(self.title_frame, font=(self.font, F_SIZE['S']))
        self.memo_title.pack(side=tk.LEFT, fill=tk.X, padx=5)

# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    root.title(TITLE)
    root.resizable(0, 0)
    # 初期表示位置指定
    sx = int(root.winfo_screenwidth()/2)
    sy = int(root.winfo_screenheight()/2)
    root.geometry("%sx%s+%s+%s" % (ROOT_WIDTH, ROOT_HEIGHT, int(sx - ROOT_WIDTH/2), int(sy - ROOT_HEIGHT/2)))
    # 開始
    app = MemoPad(master=root)
    app.mainloop()
