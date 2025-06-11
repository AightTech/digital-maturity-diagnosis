from flask import Request
from src.presentation.http_value_objects.HttpResponse import HttpResponse
from src.domain.use_case.DiagnosticGeneratorUseCase import DiagnosticGeneratorUseCase

class DiagnosticGeneratorController:
    def __init__(self, use_case: DiagnosticGeneratorUseCase):
        self.__use_case = use_case

    async def handle(self, request: Request) -> HttpResponse:
        if request: 
            request_data = request.json
        
        http_response = await self.__use_case.generate(request_data)

        return http_response