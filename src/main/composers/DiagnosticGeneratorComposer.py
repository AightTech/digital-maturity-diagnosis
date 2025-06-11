from src.infrastructure.db.repositories.NotionRepository import NotionRepository
from src.infrastructure.data_parser.WebhookTallyParser import WebhookTallyParser
from src.domain.use_case.DiagnosticGeneratorUseCase import DiagnosticGeneratorUseCase
from src. presentation.controllers.DiagnosticGeneratorController import DiagnosticGeneratorController


def diagnostic_generator_composer():
    repository = NotionRepository()
    parser = WebhookTallyParser()

    use_case = DiagnosticGeneratorUseCase(parser= parser, repository= repository)

    controller = DiagnosticGeneratorController(use_case= use_case)

    return controller.handle

