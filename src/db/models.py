from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    false,
    func,
)

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    archived = Column(Boolean, default=False, server_default=false())
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    _password = Column(String(255))
    posts = relationship("Post")


class Tag_Post(Base):
    __tablename__ = "tags_posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column("tag_id", Integer, ForeignKey("tags.id"))
    post_id = Column("post_id", Integer, ForeignKey("posts.id"))


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String(32), unique=True, nullable=False)
    posts = relationship("Post", secondary="tags_posts", back_populates="tags")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    archived = Column(Boolean, default=False, server_default=false())
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    tags = relationship("Tag", secondary="tags_posts", back_populates="posts")

    def __str__(self):
        return f"id {self.id}, title = {self.title}, user_id = {self.user_id}, tags = {self.tags}"

    def __repr__(self):
        return self.__str__()
