from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def handle_db_error(e: Exception):
    if isinstance(e, IntegrityError):
        raise HTTPException(
            status_code=400,
            detail="Database constraint violation"
        )
    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )
