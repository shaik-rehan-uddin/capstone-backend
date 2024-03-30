from flask import render_template
from . import appbuilder, db
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import ChatSession, ChatData


class ChatSessionView(ModelView):
    datamodel = SQLAInterface(ChatSession)
    list_columns = ["id", "start_time"]


class ChatDataView(ModelView):
    datamodel = SQLAInterface(ChatData)
    list_columns = ["question_asked", "answer_provided", "chat_session_id"]


appbuilder.add_view(
    ChatSessionView, "Chat Session", icon="fa-database", category="Database"
)

appbuilder.add_view(ChatDataView, "Chat Data", icon="fa-database", category="Database")


"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
