from flask import Flask, render_template, request

app = Flask(__name__)

# 首页：GET 请求
@app.route('/')
def home():
    return "你好，这是我的第一个 Flask 站！"

# 接口示例：GET
@app.route('/getdata')
def get_data():
    return {"name": "小明", "age": 20}

# 启动服务
if __name__ == '__main__':
    app.run(debug=True, port=5000)