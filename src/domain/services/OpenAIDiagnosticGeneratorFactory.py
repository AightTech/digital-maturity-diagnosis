from os import getenv
from src.config.logger_config import setup_logger
from src.errors.types.LLModelInvalidError import LLModelInvalidError
from src.domain.services.OpenAIDiagnosticGenerator import OpenAIDiagnosticGenerator

logger = setup_logger(name= "OpenAIDiagnosticGenerator")

class OpenAIDiagnosticGeneratorFactory:
    @classmethod
    def create(cls, model_name: str = "gpt") -> OpenAIDiagnosticGenerator:
        if model_name == "gpt":
            model = "gpt-4o-mini"
            model_auth_key= getenv('OPENAI_API_KEY')
            base_url= None
        else:
            message = f'O gerador de diagnóstico com modelo "{model_name}" não foi implementado.'
            logger.error(message)
            raise LLModelInvalidError(message)

        return OpenAIDiagnosticGenerator(model= model, 
                                         model_auth_key= model_auth_key,
                                         base_url= base_url)