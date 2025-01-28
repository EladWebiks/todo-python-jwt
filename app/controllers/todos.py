from fastapi import Depends, HTTPException
from app.services.todos import TodoService
from app.schemas import TodoCreate, TodoUpdate, TodoResponse

class TodoController:
    def __init__(self, service: TodoService = Depends()):
        self.service = service

    async def create(self, todo: TodoCreate) -> TodoResponse:
        return await self.service.create(todo)

    async def get_by_id(self, todo_id: str) -> TodoResponse:
        todo = await self.service.get_by_id(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    async def update(self, todo_id: str, todo: TodoUpdate) -> TodoResponse:
        updated_todo = await self.service.update(todo_id, todo)
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated_todo

    async def delete(self, todo_id: str) -> dict:
        deleted = await self.service.delete(todo_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"message": "Todo deleted"}
