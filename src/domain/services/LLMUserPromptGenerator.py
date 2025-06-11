from typing import Dict
from pathlib import Path
from string import Template
import json

class LLMUserPromptGenerator:
    def __init__(self):
        self.user_prompt_path = "src/llm_prompts/user_prompt.txt"

    def generate(self, maturity_scores: Dict, maturity_levels: Dict, markdown_text: str) -> str:
        diagnostic_prompt = Path(self.user_prompt_path).read_text(encoding='utf-8')
        template = Template(diagnostic_prompt)

        return template.substitute(
            maturity_scores = json.dumps(maturity_scores, indent=2, ensure_ascii=False),
            maturity_levels = json.dumps(maturity_levels, indent=2, ensure_ascii=False), 
            markdown_text = markdown_text
        )