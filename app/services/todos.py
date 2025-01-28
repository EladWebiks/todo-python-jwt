from app.models import Todo, TodoResponse

class TodoService:
    async def create(self, todo: Todo):
        """
        Create a new Todo item.
        """
        return await todo.insert()

    async def get_by_id(self, todo_id: str):
        """
        Get a Todo item by its ID.
        """
        return await Todo.get(todo_id)

    async def get_all(self):
        """
        Get all Todo items.
        """
        todos = await Todo.find_all().to_list()
        # Convert each Todo document into a dictionary and replace `_id` with its string equivalent
        return [
            TodoResponse(
                id=str(todo.id),
                title=todo.title,
                description=todo.description,
                completed=todo.completed
            )
            for todo in todos
        ]

    async def update(self, todo_id: str, todo_data: Todo):
        """
        Update an existing Todo item.
        """
        todo = await Todo.get(todo_id)
        if todo:
            await todo.update({"$set": todo_data.dict(exclude_unset=True)})
        return todo

    async def delete(self, todo_id: str):
        """
        Delete a Todo item by its ID.
        """
        todo = await Todo.get(todo_id)
        if todo:
            await todo.delete()
            return True
        return False
