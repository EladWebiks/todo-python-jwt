from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import local modules
from app.database import init_db
from app.routes.todos import router as todo_router
from app.routes.users import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function to manage application startup and shutdown events.
    """
    # Startup logic
    await init_db()
    print("Database connection established.")

    yield  # Application runs while the server is running

    # Shutdown logic
    print("Application is shutting down.")

# Create FastAPI app with a lifespan manager
app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)

# Register route modules
app.include_router(todo_router, prefix="/todos", tags=["Todos"])
app.include_router(user_router, prefix="/users", tags=["Users"])
