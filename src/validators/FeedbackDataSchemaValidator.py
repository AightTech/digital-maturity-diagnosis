from src.config.logger_config import setup_logger
from src.errors.types.HttpBadRequestError import HttpBadRequestError
from cerberus import Validator
from typing import Dict

logger = setup_logger(name= "FeedbackDatachemaValidator")

class FeedbackDataSchemaValidator:
    def __init__(self):
        self.schema = {
            "feedback_score": {"type": "integer", "required": True, "empty": False},
            "feedback_comment": {"type": "string", "required": False, "nullable": True},
        }
        self.validator = Validator()

    def validate(self, feedback_data: Dict) -> None:
        if not self.validator.validate(feedback_data, self.schema):
            message = f"Erro de validação dos dados de feedback: {self.validator.errors}"
            logger.error(message)
            raise HttpBadRequestError(message)
        logger.info("Os dados de feedback do formulário foram validadas com sucesso!")