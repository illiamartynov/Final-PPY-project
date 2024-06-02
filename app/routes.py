from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        new_message = Message(user=user, message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('index'))

    messages = Message.query.order_by(
        Message.timestamp.desc()).all()  # Получение всех сообщений, отсортированных по времени отправки
    return render_template('index.html', messages=messages)
