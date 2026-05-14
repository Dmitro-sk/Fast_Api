from fastapi import APIRouter, HTTPException
from src.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

# Емуляція БД
users_db = {}
user_id_counter = 1

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global user_id_counter
    new_user = {**user.model_dump(), "id": user_id_counter}
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    stored_user_data = users_db[user_id]
    updated_user = {**stored_user_data, **user_update.model_dump(exclude_unset=True)}
    users_db[user_id] = updated_user
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}