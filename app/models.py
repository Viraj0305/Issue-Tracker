from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey,
    DateTime, Table
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

issue_labels = Table(
    "issue_labels",
    Base.metadata,
    Column("issue_id", ForeignKey("issues.id"), primary_key=True),
    Column("label_id", ForeignKey("labels.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="open")
    assignee_id = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime)

    comments = relationship("Comment", cascade="all, delete")
    labels = relationship("Label", secondary=issue_labels)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    issue_id = Column(Integer, ForeignKey("issues.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# ✅ Timeline Table (BONUS)
class IssueHistory(Base):
    __tablename__ = "issue_history"
    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.id", ondelete="CASCADE"))
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
