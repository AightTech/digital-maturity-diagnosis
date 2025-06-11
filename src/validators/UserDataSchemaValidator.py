from src.config.logger_config import setup_logger
from src.errors.types.HttpBadRequestError import HttpBadRequestError
from cerberus import Validator
from typing import Dict

logger = setup_logger(name= "UserDatachemaValidator")

class UserDataSchemaValidator:
    def __init__(self):
        self.schema = {
            "responsible": {"type": "string", "required": True, "empty": False},
            "email": {"type": "string", "required": True, "empty": False},
            "phone": {"type": "string", "required": True, "empty": False},
            "business_name": {"type": "string", "required": True, "empty": False},
            "sector": {"type": "string", "required": True, "empty": False},
            "business_description": {"type": "string", "required": True, "empty": False},
            "num_employees": {"type": "integer", "required": True, "empty": False},
            "monthly_billing": {"type": "string", "required": True, "empty": False}
        }
        self.validator = Validator()

    def validate(self, user_data: Dict) -> None:
        if not self.validator.validate(user_data, self.schema):
            message = f"Erro de validação nos dados de identificação do usuário: {self.validator.errors}"
            logger.error(message)
            raise HttpBadRequestError(message)
        logger.info("Os dados do usuário do formulário foram validadas com sucesso!")