from .database import SessionLocal

# Dependency that provides a database session and ensures it is properly closed after each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
