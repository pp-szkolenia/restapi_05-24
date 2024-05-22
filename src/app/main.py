from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


from app.routers import tasks, users, auth


app = FastAPI(docs_url="/api/docs",
              redoc_url="/api/redoc",
              title="Task manager API",
              description="API for managing tasks",
              version="1.0.2")

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Hello world!"})
