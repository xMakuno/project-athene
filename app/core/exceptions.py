from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Override the default 422 validation error to return a cleaner format.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": "Validation Error",
            "errors": [
                {
                    "field": ".".join(str(x) for x in error["loc"]),
                    "message": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        },
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Override default HTTP exceptions to match our standard format.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
        },
    )
