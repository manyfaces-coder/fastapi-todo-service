from fastapi import FastAPI
import uvicorn
from api.routers.auth import auth_router
from api.routers.todo import todo_router
from api.routers.attachment import attachment_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(attachment_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)