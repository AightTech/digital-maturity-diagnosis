from typing import Dict
from src.config.logger_config import setup_logger
from src.presentation.http_value_objects.HttpResponse import HttpResponse
from src.infrastructure.interfaces.DiagnosticRepositoryInterface import DiagnosticRepositoryInterface
from src.infrastructure.interfaces.FormResponseParserInterface import FormResponseParserInterface
from src.domain.services.FormResponseFactory import FormResponseFactory
from src.domain.services.DigitalMaturityScoresCalculator import DigitalMaturityScoresCalculator
from src.domain.services.DigitalMaturityLevelClassifier import DigitalMaturityClassesClassifier
from src.domain.services.DimensionDataToMarkdownConverter import DimensionDataToMarkdownConverter
from src.domain.services.LLMUserPromptGenerator import LLMUserPromptGenerator
from src.domain.services.OpenAIDiagnosticGeneratorFactory import OpenAIDiagnosticGeneratorFactory
from src.domain.services.RadarPlotGenerator import RadarPlotGenerator
from src.domain.services.DiagnosticResponseToPDFConverter import DiagnosticResponseToPDFConverter
from src.domain.services.TempFilesDeleter import TempFilesDeleter

logger = setup_logger(name= "DiagnosticGeneratorUseCase")

class DiagnosticGeneratorUseCase:
    def __init__(self, parser: FormResponseParserInterface,
                 repository: DiagnosticRepositoryInterface):
        self.__parser = parser
        self.__repository = repository
        self.temp_folder_path = 'src/tmp/'

    async def generate(self, request_data: Dict) -> HttpResponse:
        form_response_data_parsed = self.__parser.parse(request_data= request_data)

        form_response_factory = FormResponseFactory()
        form_response = form_response_factory.create(**form_response_data_parsed)

        indexes_calculator = DigitalMaturityScoresCalculator()
        maturity_scores = indexes_calculator.calculate(form_response)

        maturity_classifier = DigitalMaturityClassesClassifier()
        maturity_levels = maturity_classifier.classify(maturity_scores)

        markdown_converter = DimensionDataToMarkdownConverter()
        markdown_text = markdown_converter.convert(form_response)

        user_prompt_generator = LLMUserPromptGenerator()
        user_prompt = user_prompt_generator.generate(maturity_scores= maturity_scores,
                                                     maturity_levels= maturity_levels,
                                                     markdown_text= markdown_text)

        open_ai_diagnostic_generator_factory = OpenAIDiagnosticGeneratorFactory()
        open_ai_diagnostic_generator = open_ai_diagnostic_generator_factory.create(model_name= "gpt")
        diagnostic_response = await open_ai_diagnostic_generator.generate(user_prompt= user_prompt)

        radar_plot_generator = RadarPlotGenerator(self.temp_folder_path)
        radar_plot_file_path = radar_plot_generator.generate(maturity_scores)

        pdf_converter = DiagnosticResponseToPDFConverter(self.temp_folder_path)
        pdf_name, pdf_path = pdf_converter.convert(diagnostic_response = diagnostic_response,
                                                   maturity_scores= maturity_scores, 
                                                   maturity_levels= maturity_levels,
                                                   radar_plot_file_path= radar_plot_file_path)
        
        http_response = await self.__repository.store_diagnostic(form_response= form_response,
                                                 pdf_name= pdf_name, pdf_path= pdf_path)

        temp_file_paths_list = [pdf_path, radar_plot_file_path]

        temp_files_deleter = TempFilesDeleter()
        temp_files_deleter.delete(temp_file_paths_list)

        logger.info("Fim da aplicação!")

        return http_response
    
