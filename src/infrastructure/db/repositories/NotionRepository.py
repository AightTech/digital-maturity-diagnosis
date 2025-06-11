import os
import json
import requests
from typing import Dict
from notion_client import AsyncClient
from src.config.logger_config import setup_logger
from src.errors.types.HttpServerError import HttpServerError
from src.domain.entities.FormResponse import FormResponse
from src.presentation.http_value_objects.HttpResponse import HttpResponse
from src.infrastructure.interfaces.DiagnosticRepositoryInterface import DiagnosticRepositoryInterface

logger = setup_logger(name= "NotionRepository")

class NotionRepository(DiagnosticRepositoryInterface):
    def __init__(self):
        notion_api_key = os.getenv('NOTION_API_KEY')
        self.notion_client = AsyncClient(auth= notion_api_key)

    async def store_diagnostic(self, form_response: FormResponse, pdf_name: str, pdf_path: str) -> HttpResponse:
        file_upload_obj_id = self.__create_file_upload_object(pdf_name)

        self.__send_file_upload(file_upload_obj_id= file_upload_obj_id,
                                pdf_name= pdf_name, pdf_path= pdf_path)

        response = await self.__save_complete_diagnostic(file_upload_obj_id= file_upload_obj_id,
                                                         user_data= form_response.user_data, 
                                                         feedback_data= form_response.feedback_data, 
                                                         pdf_name= pdf_name)
        
        logger.info("O diagnóstico foi armazenado com sucesso!")
        return HttpResponse(status_code= 200, body= {"data": {"page_id": response.get('id')}})
    
    @classmethod
    def __create_file_upload_object(cls, pdf_name) -> str:
        url = "https://api.notion.com/v1/file_uploads"

        payload = {
            "filename": pdf_name,
            "content_type": "application/pdf"
        }

        headers = {
            "Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}",
            "accept": "application/json",
            "content-type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        try: 
            response = requests.post(url, json= payload, headers= headers)
        except Exception as e:
            message = f"Falha ao criar File Upload Object: [{e}]"
            logger.error(message)

        if response.status_code != 200:
            message = f"Falha ao criar File Upload Object: {response.text}"
            logger.error(message)
            raise  HttpServerError(message, status_code= response.status_code)

        file_upload_obj_id = json.loads(response.text)['id']

        return file_upload_obj_id

    @classmethod
    def __send_file_upload(cls, file_upload_obj_id: str, pdf_name: str, pdf_path: str) -> None:
        url = f"https://api.notion.com/v1/file_uploads/{file_upload_obj_id}/send"

        headers = {
            "Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}",
            "Notion-Version": "2022-06-28"
        }

        with open(pdf_path, "rb") as f:
            files = {
                "file": (pdf_name, f, "application/pdf")
            }

            try:
                response = requests.post(url= url, headers= headers, files= files)
            except Exception as e:
                message = f"Falha de upload do PDF: [{e}]"
                logger.error(message)

            if response.status_code != 200:
                message = f"Falha de upload do PDF: {response.text}"
                logger.error(message)
                raise HttpServerError(message, status_code= response.status_code)
            
        return None
    

    async def __save_complete_diagnostic(self, file_upload_obj_id: str, user_data: Dict, feedback_data: Dict, pdf_name: str) -> None:
        response = await self.notion_client.pages.create(
            icon = {
                "type": "emoji",
                "emoji": "📋"
            },
            parent= {
                "type": "database_id",
                "database_id": os.getenv('NOTION_DB_ID')
            },
            properties= {
                'Responsável': {
                    'title': [{"text": {"content": user_data.get('responsible')}}]
                },
                'E-mail': {
                    'email': user_data.get('email')
                },
                'Telefone': {
                    'phone_number': user_data.get('phone')
                },
                'Nome da Empresa': {
                    'rich_text': [{"text": {"content": user_data.get('business_name')}}]
                },
                'Área de Atuação': {
                    'select': {"name": user_data.get('sector')}
                },
                'Descrição do Negócio': {
                    'rich_text': [{"text": {"content": user_data.get('business_description')}}]
                },
                'Nº de Colaboradores': {
                    'number': user_data.get('num_employees')
                },
                'Faturamento Mensal': {
                    'select': {"name": user_data.get('monthly_billing')}
                },
                'Nota de Satisfação': {
                    'number': feedback_data.get('feedback_score')
                },
                'Experiência do Cliente': {
                    'rich_text': [{"text": {"content": feedback_data.get('feedback_comment')}}]
                },
                'Diagnóstico': {
                    'files': [
                        {
                        "type": "file_upload",
                        "file_upload": { "id": file_upload_obj_id},
                        "name": pdf_name
                        }
                    ]
                }
            }
        )

        if response.get('object', None) in ["error", None]:
            if not response:
                message_when_is_none = f"Falha na criação da Página de Diagnóstico. Reposta vazia."
                logger.error(message_when_is_none)
                raise HttpServerError(message_when_is_none)
            
            message_when_is_error = f"Falha na criação da Página de Diagnóstico [{response.code}]: {response.message}"
            logger.error(message_when_is_error)
            raise HttpServerError(message_when_is_error, status_code= response.status)
        
        return response
        