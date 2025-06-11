from abc import ABC, abstractmethod
from typing import Dict

class FormResponseParserInterface(ABC):
    @abstractmethod
    def parse(self, request_data: Dict) -> Dict:
        pass