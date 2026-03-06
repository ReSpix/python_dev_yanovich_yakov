from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    login: Mapped[str] = mapped_column(String, nullable=False)

    blogs: Mapped[list["Blog"]] = relationship("Blog", back_populates="owner")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="commentator"
    )


class Blog(Base):
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="blogs")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="blog")


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    header: Mapped[str | None] = mapped_column(String, nullable=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    blog_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog.id"), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    blog: Mapped["Blog"] = relationship("Blog", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commentator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)

    commentator: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
