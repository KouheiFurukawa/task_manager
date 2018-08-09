# DB
import sqlite3
import os

# アプリ定数
DBMANE = 'database/database.db'

# ---------------------------------------------------------------------------
# dbmodule
#
# データベース操作用の関数を分離
# ---------------------------------------------------------------------------
# データベース生成
# ---------------------------------------------------------------------------
def create_database():
    # ディレクトリ確認
    try:
        os.makedirs('database')
    except:
        pass
    c = sqlite3.connect(DBMANE)
    c.execute("PRAGMA foreign_keys = ON")
    try:
        # itemテーブルの定義
        ddl = """
        CREATE TABLE items
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            maintext TEXT,
            ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        c.execute(ddl)
    except:
        print('作成エラー')
    c.commit()
    c.close()

# ---------------------------------------------------------------------------
# メモ全件取得
# ---------------------------------------------------------------------------
def select_memo():
    result = []
    c = sqlite3.connect(DBMANE)
    c.execute("PRAGMA foreign_keys = ON")
    try:
        sql = """
        SELECT id, name, maintext
        FROM items
        """
        result = c.execute(sql)
        print('取得完了')
    except:
        print('取得エラー')
    return list(result)

# ---------------------------------------------------------------------------
# メモ1件取得
# ---------------------------------------------------------------------------
def select_memo_one(id):
    result = []
    c = sqlite3.connect(DBMANE)
    c.execute("PRAGMA foreign_keys = ON")
    try:
        sql = """
        SELECT id, name, maintext
        FROM items
        WHERE id = {}
        """.format(id)
        result = c.execute(sql)
        print('取得完了')
    except:
        print('取得エラー')
    return list(result)

# ---------------------------------------------------------------------------
# メモ登録
# ---------------------------------------------------------------------------
def insert_memo(memo):
    c = sqlite3.connect(DBMANE)
    try:
        print(memo)
        sql = """
        INSERT INTO items(name, category_id, maintext)
        VALUES('{}', {}, '{}')
        """.format(memo[0], 1, memo[1])
        print(sql)
        c.execute(sql)
        c.commit()
        c.close()
        print('登録成功')
    except:
        print('登録エラー')

# ---------------------------------------------------------------------------
# メモ編集
# ---------------------------------------------------------------------------
def update_memo(memo):
    c = sqlite3.connect(DBMANE)
    c.execute("PRAGMA foreign_keys = ON")
    try:
        print(memo)
        sql = """
        UPDATE items
        SET name = '{}', category_id = {}, maintext = '{}'
        WHERE id = {}
        """.format(memo[0], memo[1], memo[2], memo[3])
        c.execute(sql)
        c.commit()
        c.close()
        print('更新成功')
    except:
        print('更新エラー')

# ---------------------------------------------------------------------------
# メモ削除
# ---------------------------------------------------------------------------
def delete_memo(id):
    c = sqlite3.connect(DBMANE)
    c.execute("PRAGMA foreign_keys = ON")
    try:
        sql = """
        DELETE FROM items
        WHERE id = {}
        """.format(id)
        c.execute(sql)
        c.commit()
        c.close()
        print('削除成功')
    except:
        print('削除エラー')
