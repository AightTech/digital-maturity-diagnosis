from typing import Dict
from pathlib import Path
from openai import AsyncOpenAI
from src.config.logger_config import setup_logger
from src.domain.value_objects.DiagnosisOutput import DiagnosisOutput

logger = setup_logger(name= "OpenAIDiagnosticGenerator")

class OpenAIDiagnosticGenerator:
    def __init__(self, model: str, model_auth_key: str, base_url: str):
        self.model = model
        self.model_auth_key = model_auth_key
        self.base_url = base_url
        self.system_prompt_path = "src/llm_prompts/system_prompt.txt"

    async def generate(self, user_prompt: str, 
                       temperature: float= 0.3, 
                       max_output_tokens: int= 8126) -> Dict:
        system_prompt = Path(self.system_prompt_path).read_text(encoding='utf-8')
        try: 
            openai_client = AsyncOpenAI(api_key= self.model_auth_key, base_url= self.base_url)

            response = await openai_client.responses.parse(
                model= self.model,
                temperature= temperature,
                max_output_tokens= max_output_tokens,
                input= [
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user',
                        'content': user_prompt
                    }
                ],
                text_format= DiagnosisOutput
            )

            logger.info("O diagnóstico foi criado com sucesso pela LLM!")
            
        except Exception as e:
            logger.error(f"Falha ao gerar diagnóstico pela LLM: [{e}]")

        return response.output_parsed.model_dump()