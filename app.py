from flask import Flask, render_template, request, redirect, url_for, session
import os
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Initialize the To-Do list
todo_list = []

# Load the To-Do list if the file exists
if os.path.exists('todo_list.pkl'):
    with open('todo_list.pkl', 'rb') as f:
        todo_list = pickle.load(f)

@app.route('/')
def index():
    # Default theme mode is dark
    theme = session.get('theme', 'dark')
    return render_template('index.html', todo_list=todo_list, theme=theme)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']
    
    # Validate email and priority
    if '@' in email and priority in ['Low', 'Medium', 'High']:
        todo_list.append({'task': task, 'email': email, 'priority': priority})
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    todo_list.clear()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(todo_list):
        del todo_list[task_id]
    return redirect(url_for('index'))

@app.route('/save')
def save():
    with open('todo_list.pkl', 'wb') as f:
        pickle.dump(todo_list, f)
    return redirect(url_for('index'))

@app.route('/toggle-theme')
def toggle_theme():
    current_theme = session.get('theme', 'dark')
    session['theme'] = 'light' if current_theme == 'dark' else 'dark'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
