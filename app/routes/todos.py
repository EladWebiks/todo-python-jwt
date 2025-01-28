from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.auth.auth_bearer import JWTBearer
from app.models import Todo, TodoCreate, TodoUpdate

router = APIRouter()

@router.post("/", dependencies=[Depends(JWTBearer())], response_model=Todo)
async def create_todo(todo_data: TodoCreate):
    """
    Create a new Todo item.
    """
    todo = Todo(**todo_data.dict())
    created_todo = await todo.insert()
    return created_todo

@router.get("/", dependencies=[Depends(JWTBearer())], response_model=List[Todo])
async def get_all_todos():
    """
    Get all Todo items.
    """
    todos = await Todo.find_all().to_list()
    return todos

@router.get("/{todo_id}", dependencies=[Depends(JWTBearer())], response_model=Todo)
async def get_todo(todo_id: str):
    """
    Get a Todo item by its ID.
    """
    todo = await Todo.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", dependencies=[Depends(JWTBearer())], response_model=Todo)
async def update_todo(todo_id: str, todo_data: TodoUpdate):
    """
    Update an existing Todo item.
    """
    todo = await Todo.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await todo.update({"$set": todo_data.dict(exclude_unset=True)})
    return todo

@router.delete("/{todo_id}",dependencies=[Depends(JWTBearer())])
async def delete_todo(todo_id: str):
    """
    Delete a Todo item by its ID.
    """
    todo = await Todo.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await todo.delete()
    return {"message": "Todo deleted"}
