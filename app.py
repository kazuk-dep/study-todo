from flask import Flask,render_template,g,redirect,request
import sqlite3
DATEBASE="datebase.db"

app = Flask(__name__)

import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # ← 行を辞書っぽく扱えるようにするやつ（便利）
    return conn


# 📌 タスク一覧を表示
@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


# 📌 タスクを追加する
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]  # ← フォームから "title" を受け取る
    if title:
        conn = get_db_connection()
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
    return redirect("/")  # 追加後、トップページにリダイレクト

@app.route("/edit/<id>")
def edit_task(id):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id=?",(id,)).fetchone()
    conn.commit()
    conn.close()
    return render_template("edit.html",task=task)

@app.route("/update/<id>",methods=["POST"])
def update_task(id):
    new_title = request.form["title"]
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET title=? WHERE id=? ",(new_title,id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<id>")
def delete_task(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# ← ここが「complete」の処理！
@app.route("/complete/<id>")
def complete_task(id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)