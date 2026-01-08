from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import issues, reports, timeline

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Issue Tracker API")

app.include_router(issues.router)
app.include_router(reports.router)
app.include_router(timeline.router)
