from src.config.logger_config import setup_logger
from src.errors.types.HttpBadRequestError import HttpBadRequestError
from cerberus import Validator
from typing import List, Dict

logger = setup_logger(name= "DimensionDataSchemaValidator")

class DimensionDataSchemaValidator:
    def __init__(self):
        self.schema = {
            "dimension_name": {"type": "string", "required": True, "empty": False},
            "responses": {
                "type": "dict",
                "required": True,
                "keysrules": {"type": "string"},
                "valuesrules": {"type": ["string", "integer"], "nullable": True}
            },
            "textarea_counts": {"type": "integer", "required": False}
        }
        self.validator = Validator()

    def validate(self, dimension_data: List[Dict]) -> None:
        for data in dimension_data:
            if not self.validator.validate(data, self.schema):
                message = f"Erro de validação dos dados das dimensões do formulário: {self.validator.errors}"
                logger.error(message)
                raise HttpBadRequestError(message)
        logger.info("Os dados de todas as dimensões do formulário foram validadas com sucesso!")