from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, workflow
from app.db.session import engine
from app.db import base

base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Integrated ERP System API",
    description="Backend services for the ERP desktop application.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(workflow.router, prefix="/api", tags=["Workflow & Data"])

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ERP Backend is running successfully"}

@app.get("/ "), tags=[Invnto]