from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


class ChatSession(db.Model):
    __tablename__ = "chat_sessions"

    id = db.Column(db.String(36), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    chat_data = db.relationship("ChatData", backref="chat_session", lazy=True)

    def json(self):
        return {"id": self.id, "start_time": self.start_time.isoformat()}


class ChatData(db.Model):
    __tablename__ = "chat_data"

    id = db.Column(db.String(36), primary_key=True)
    question_asked = db.Column(db.Text, nullable=False)
    answer_provided = db.Column(db.Text, nullable=False)
    chat_session_id = db.Column(
        db.String(36), db.ForeignKey("chat_sessions.id"), nullable=False
    )

    def json(self):
        return {
            "id": self.id,
            "question_asked": self.question_asked,
            "answer_provided": self.answer_provided,
        }
