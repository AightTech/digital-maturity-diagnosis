from abc import ABC, abstractmethod
from src.domain.entities.FormResponse import FormResponse
from src.presentation.http_value_objects.HttpResponse import HttpResponse

class DiagnosticRepositoryInterface(ABC):
    @abstractmethod
    def store_diagnostic(self, form_response: FormResponse, pdf_name: str, pdf_path: str) -> HttpResponse:
        pass