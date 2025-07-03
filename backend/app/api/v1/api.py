from fastapi import APIRouter
from app.api.v1.endpoints import auth, prompts, optimizations, templates, analytics, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(optimizations.router, prefix="/optimizations", tags=["optimizations"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"]) 