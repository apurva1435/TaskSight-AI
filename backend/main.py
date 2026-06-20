from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes.analyze import router as analyze_router
from routes.compare import router as compare_router
from routes.history import router as history_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve outputs folder
app.mount(
    "/outputs",
    StaticFiles(directory="../outputs"),
    name="outputs"
)

@app.get("/")
def home():
    return {
        "message": "TaskSight AI Backend Running"
    }

# Register routes
app.include_router(analyze_router)

app.include_router(compare_router)

app.include_router(history_router)