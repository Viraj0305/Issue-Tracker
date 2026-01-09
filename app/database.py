from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL database connection URL
DATABASE_URL = "postgresql://issue_user:password@localhost:5432/issues_db"

# Create SQLAlchemy engine to manage database connections
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
