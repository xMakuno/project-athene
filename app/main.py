from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.logging import setup_logging
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException as FastAPIHTTPException
from app.core.exceptions import validation_exception_handler, http_exception_handler

# Initialize logging immediately
logger = setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Register custom exception handlers
    # app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # app.add_exception_handler(FastAPIHTTPException, http_exception_handler)

    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    @app.get("/")
    def read_root():
        return {"message": "Welcome to Project Athene"}
    
    return app

app = create_app()
