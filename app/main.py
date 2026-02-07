from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.features.bookings.router import router as bookings_router
from app.features.routes.router import router as routes_router
from app.features.shipments.router import router as shipments_router
from app.features.vessels.router import router as vessels_router
from app.shared.api_response import api_response

app = FastAPI()

app.include_router(vessels_router, prefix="/api")
app.include_router(bookings_router, prefix="/api")
app.include_router(routes_router, prefix="/api")
app.include_router(shipments_router, prefix="/api")


def _format_validation_errors(exc: RequestValidationError) -> str:
    errors = []
    for err in exc.errors():
        loc = ".".join(str(x) for x in err["loc"] if x != "body")
        msg = err.get("msg", "Validation error")
        errors.append(f"{loc}: {msg}" if loc else msg)
    return "; ".join(errors)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_message = _format_validation_errors(exc)
    return JSONResponse(
        status_code=422,
        content=api_response(success=False, error=error_message),
    )
