from fastapi import APIRouter, Depends, HTTPException, UploadFile,Body
from sqlalchemy.orm import Session
from datetime import datetime
import csv
from ..utils import handle_db_error
from ..models import Issue, Comment, Label, IssueHistory,User
from ..schemas import *
from ..deps import get_db

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.post("/bulk-status")
def bulk_status(data: BulkStatus, db: Session = Depends(get_db)):
    try:
        for issue_id in data.issue_ids:
            issue = db.get(Issue, issue_id)
            if not issue:
                raise ValueError
            issue.status = data.status
        db.commit()
    except:
        db.rollback()
        raise HTTPException(400, "Bulk update failed")
    return {"updated": len(data.issue_ids)}

@router.post("/import")
def import_csv(file: UploadFile, db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(content)

    created = 0
    errors = []

    for i, row in enumerate(reader, start=1):
        if not row.get("title"):
            errors.append({
                "row": i,
                "error": "Title missing"
            })
            continue

        try:
            issue = Issue(title=row["title"])
            db.add(issue)
            created += 1
        except Exception:
            errors.append({
                "row": i,
                "error": "Database error"
            })

    db.commit()

    return {
        "created": created,
        "failed": len(errors),
        "errors": errors
    }


@router.post("")
def create_issue(data: IssueCreate, db: Session = Depends(get_db)):
    issue = Issue(**data.dict())
    db.add(issue)
    db.commit()
    db.refresh(issue)

    db.add(IssueHistory(issue_id=issue.id, action="Issue created"))
    db.commit()

    return issue

@router.get("")
def list_issues(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return db.query(Issue).offset(skip).limit(limit).all()

@router.get("/{issue_id}")
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(404, "Issue not found")
    return issue



@router.patch("/{issue_id}")
def update_issue(
    issue_id: int,
    data: IssueUpdate = Body(...),
    db: Session = Depends(get_db)
):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if issue.version != data.version:
        raise HTTPException(status_code=409, detail="Version conflict")

    if data.title is not None:
        issue.title = data.title
        db.add(IssueHistory(issue_id=issue.id, action="Title updated"))

    if data.status is not None and data.status != issue.status:
        issue.status = data.status
        db.add(IssueHistory(issue_id=issue.id, action=f"Status changed to {data.status}"))

    issue.version += 1
    db.commit()
    return issue

@router.post("/{issue_id}/comments")
def add_comment(issue_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    user = db.get(User, data.author_id)
    if not user:
        raise HTTPException(status_code=400, detail="Author does not exist")

    try:
        comment = Comment(issue_id=issue_id, **data.dict())
        db.add(comment)
        db.commit()
        return comment
    except Exception as e:
        db.rollback()
        handle_db_error(e)

@router.put("/{issue_id}/labels")
def replace_labels(issue_id: int, labels: list[str], db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    issue.labels.clear()

    for name in labels:
        label = db.query(Label).filter_by(name=name).first()
        if not label:
            label = Label(name=name)
        issue.labels.append(label)

    db.add(IssueHistory(issue_id=issue.id, action="Labels updated"))
    db.commit()
    return issue
