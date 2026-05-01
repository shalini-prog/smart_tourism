from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import crowd_routes

app = FastAPI(title="AI Smart Tourism System")

# ==============================
# CORS CONFIGURATION
# ==============================
# Allow frontend (Vite) to access backend
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# ROUTERS
# ==============================
app.include_router(crowd_routes.router)

# ==============================
# ROOT ENDPOINT
# ==============================
@app.get("/")
def root():
    return {"message": "AI Tourist Flow Optimization Backend Running"}