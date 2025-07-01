from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/check") 
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    try:
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))