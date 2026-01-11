from fastapi import APIRouter

router = APIRouter()

@router.get("/jira/sync")
async def sync_jira():
    return {"status": "success", "message": "Jira data synced (Simulated)"}
