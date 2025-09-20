from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="Concurso AI API",
    description="API para sistema de simulados de concursos públicos",
    version="1.0.0"
)

# Configure CORS origins based on environment
cors_origins = [settings.frontend_url]

# Add production origins if in production
if settings.environment == "production":
    cors_origins.extend([
        "https://concurso-ai-frontend.vercel.app",
        "https://concurso-ai.vercel.app",
        "https://*.vercel.app"
    ])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (with error handling)
try:
    from app.routers import auth, simulados, dashboard
    app.include_router(auth.router)
    app.include_router(simulados.router)
    app.include_router(dashboard.router)
except Exception as e:
    print(f"Warning: Could not load routers: {e}")
    # App will still start with basic endpoints


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Concurso AI API is running!"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/init-db")
def init_database():
    """Initialize database with seed data"""
    try:
        from init_db import main as init_db_main
        init_db_main()
        return {"message": "Database initialized successfully"}
    except Exception as e:
        return {"error": str(e)}
