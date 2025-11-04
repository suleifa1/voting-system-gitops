from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"users": [], "message": "Get all users"}

@router.get("/polls")
async def get_all_polls():
    return {"polls": [], "message": "Admin: Get all polls"}

@router.delete("/polls/{poll_id}")
async def admin_delete_poll(poll_id: int):
    return {"message": f"Admin deleted poll {poll_id}"}

@router.get("/stats")
async def get_stats():
    return {"stats": {"total_polls": 0, "total_votes": 0, "total_users": 0}}