from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 模拟数据库
stakeholders = []
ENGAGEMENT_LEVELS = ['不觉察', '抵触', '中立', '支持', '领导']

@app.route('/')
def index():
    return render_template('index.html', stakeholders=stakeholders, levels=ENGAGEMENT_LEVELS)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    role = request.form.get('role')
    power = request.form.get('power')
    interest = request.form.get('interest')
    current_eng = request.form.get('current_eng')
    desired_eng = request.form.get('desired_eng')
    
    if name and role:
        stakeholders.append({
            'id': len(stakeholders) + 1,
            'name': name,
            'role': role,
            'power': power,
            'interest': interest,
            'current_eng': current_eng,
            'desired_eng': desired_eng
        })
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    global stakeholders
    stakeholders = [s for s in stakeholders if s['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
