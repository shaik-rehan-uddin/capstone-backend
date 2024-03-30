import uuid
import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, String, Text
from sqlalchemy.orm import relationship


class ChatSession(Model):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True)
    start_time = Column(Date, default=datetime.datetime.utcnow, nullable=False)
    chat_data = relationship("ChatData", backref="chat_session", lazy="dynamic")

    def __repr__(self):
        return f"ChatSession {self.id}"


class ChatData(Model):
    __tablename__ = "chat_data"

    id = Column(String(36), primary_key=True)
    question_asked = Column(Text, nullable=False)
    answer_provided = Column(Text, nullable=False)
    chat_session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)

    def __repr__(self):
        return f"ChatData {self.id}"
