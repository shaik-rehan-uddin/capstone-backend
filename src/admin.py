from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, ChatSession, ChatData

admin = Admin(name="Admin Panel", template_mode="bootstrap3")

# Add views for each model
admin.add_view(ModelView(ChatSession, db.session))
admin.add_view(ModelView(ChatData, db.session))
