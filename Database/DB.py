from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

connector = SQLAlchemy()

class Messages(connector.Model):
    id = connector.Column(connector.Integer, primary_key=True)
    username = connector.Column(connector.String(100), nullable=False)
    email = connector.Column(connector.String(127), nullable=False)
    subject = connector.Column(connector.String(100), nullable=False)
    message = connector.Column(connector.Text, nullable=False)
    date = connector.Column(connector.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<User {self.username}>'