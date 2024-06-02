from datetime import datetime
from app import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Поле для времени отправки

    def __repr__(self):
        return f"<Message {self.user}: {self.message} at {self.timestamp}>"
