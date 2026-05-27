from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 数据库连接（通用函数）
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row  # 让结果可以用字段名访问
    return conn

# 初始化表（第一次运行自动创建）
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 首页：学生列表
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    if not students:
        students = []  # 确保students是一个列表，即使没有数据
    conn.close()
    return render_template('index.html', students=students)

# 添加学生页面
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO students (name, age, gender) VALUES (?, ?, ?)',
            (name, age, gender)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# 编辑学生
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']

        conn.execute(
            'UPDATE students SET name=?, age=?, gender=? WHERE id=?',
            (name, age, gender, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', student=student)

# 删除学生
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # 启动时自动建表
    app.run(debug=True)