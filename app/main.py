from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import issues, reports, timeline

# Create all database tables based on SQLAlchemy models
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application with metadata
app = FastAPI(title="Issue Tracker API")

# Register application routers
app.include_router(issues.router)
app.include_router(reports.router)
app.include_router(timeline.router)
