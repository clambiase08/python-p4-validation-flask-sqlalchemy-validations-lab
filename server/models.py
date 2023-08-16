from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    __tableargs__ = UniqueConstraint("name", name="uix_1")

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("No name specified")
        return value

    @validates("phone_number")
    def validate_phone_number(self, key, value):
        if not len(value) == 10:
            raise ValueError("Invalid phone number")
        return value

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title")
    def validate_title(self, key, value):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(string in value for string in clickbait):
            raise ValueError("No title specified")
        return value

    @validates("content")
    def validate_content(self, key, value):
        if not len(value) >= 250:
            raise ValueError("Content must be at least 250 characters")
        return value

    @validates("summary")
    def validate_summary(self, key, value):
        if not len(value) < 250:
            raise ValueError("Summary must be less than 250 characters")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if value != "Fiction" and value != "Non-Fiction":
            raise ValueError("Invalid category")
        return value

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"
