from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, simulados, dashboard

# Create FastAPI app
app = FastAPI(
    title="Concurso AI API",
    description="API para sistema de simulados de concursos públicos",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(simulados.router)
app.include_router(dashboard.router)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Concurso AI API is running!"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
