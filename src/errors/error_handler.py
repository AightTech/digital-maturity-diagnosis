from src.config.logger_config import setup_logger
from src.presentation.http_value_objects.HttpResponse import HttpResponse
from src.errors.types.HttpBadRequestError import HttpBadRequestError
from src.errors.types.HttpServerError import HttpServerError
from src.errors.types.LLModelInvalidError import LLModelInvalidError

logger = setup_logger(name= "errors_handler")

def error_handler(error: Exception) -> HttpResponse:
    if isinstance(error, (HttpBadRequestError, HttpServerError, LLModelInvalidError)):
        logger.error("Erro capturado e tratado pelo handler.")
        
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )

    return HttpResponse(
        status_code=500,
        body={
            "errors": [{
                "title": "Server Error",
                "detail": str(error)
            }]
        }
    )