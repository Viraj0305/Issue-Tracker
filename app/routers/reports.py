from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Issue
from ..deps import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])

# TOP ASSIGNEES REPORT
@router.get("/top-assignees")
def top_assignees(db: Session = Depends(get_db)):
    """
    Returns assignees with the number of issues assigned to them.
    Unassigned issues are excluded from the report.
    """

    rows = (
        db.query(
            Issue.assignee_id,
            func.count(Issue.id).label("count")
        )
        .filter(Issue.assignee_id.isnot(None))   # 🔑 FIX HERE
        .group_by(Issue.assignee_id)
        .all()
    )

    return [
        {
            "assignee_id": r.assignee_id,
            "issue_count": r.count
        }
        for r in rows
    ]


# AVERAGE RESOLUTION TIME REPORT
@router.get("/latency")
def avg_resolution_time(db: Session = Depends(get_db)):
    avg_time = db.query(
        func.avg(Issue.closed_at - Issue.created_at)
    ).scalar()

    return {
        "average_resolution_time": str(avg_time) if avg_time else None
    }
