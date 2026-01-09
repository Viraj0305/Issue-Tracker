from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import IssueHistory
from ..deps import get_db

router = APIRouter(prefix="/issues", tags=["Timeline"])

#TIMELINE OF AN ISSUE
@router.get("/{issue_id}/timeline")
def get_issue_timeline(issue_id: int, db: Session = Depends(get_db)):
    return (
        db.query(IssueHistory)
        .filter(IssueHistory.issue_id == issue_id)
        .order_by(IssueHistory.timestamp)
        .all()
    )
