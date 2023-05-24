from flask_poetry_api import db


class CourseModel(db.Model):
    __tablename__ = 'courses'

    id: int = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.String(180), nullable=False)
