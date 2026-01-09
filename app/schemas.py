from pydantic import BaseModel, Field
from typing import List, Optional

class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None

class IssueUpdate(BaseModel):
    title: Optional[str] = None   
    status: Optional[str] = None 
    assignee_id: Optional[int] = None
    version: int

class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1)
    author_id: int

class BulkStatus(BaseModel):
    issue_ids: List[int]
    status: str
