from src.infrastructure.interfaces.FormResponseParserInterface import FormResponseParserInterface
from src.errors.types.HttpBadRequestError import HttpBadRequestError
from src.config.logger_config import setup_logger
from typing import List, Dict

logger = setup_logger(name= "WebhookTallyParser")

class WebhookTallyParser(FormResponseParserInterface):

    def parse(self, request_data: Dict) -> Dict:
        form_answers_data = request_data['data']['fields']

        dimensions_data = self.__build_dimensions_data(form_answers_data)
        user_data = self.__extract_user_data(dimensions_data)
        feedback_data = self.__extract_feedback_data(dimensions_data)

        form_response_data_parsed = {"user_data": user_data,
                                     "dimensions_data": dimensions_data,
                                     "feedback_data": feedback_data}
        
        logger.info("O parseamento da requisição foi realizada com sucesso!")

        return form_response_data_parsed
    
    @classmethod
    def __add_textarea_counts_in_data_struct(cls, processed_data: List[Dict], dimension_name: str, textarea_input_counts: int) -> None:
        for data in processed_data:
            if data.get('dimension_name') == dimension_name:
                data['textarea_counts'] = textarea_input_counts

    @classmethod
    def __extract_selected_response_value_text(cls, options: List[Dict], id: str) -> str:
        for option in options:
            if option.get('id') == id:
                return option.get('text')
            
    @classmethod
    def __add_response_data_in_data_struct(cls, processed_data: List[Dict], dimension_name: str, response_label: str, response_value: str) -> None:
        for prop in processed_data:
            if prop.get('dimension_name') == dimension_name:
                prop['responses'][response_label] = response_value
    

    def __build_dimensions_data(self, form_answers_data: List[Dict]) -> List[Dict]:
        processed_data_list = []
        textarea_input_counts = 0

        for data in form_answers_data:
            response_label = data.get('label').rstrip('\n')
            response_value = data.get('value')
            type_response = data.get('type')
                
            if response_label == 'Nome da Dimensão':
                if (textarea_input_counts > 0) and (dimension_name != "Identificação do Usuário"):
                    self.__add_textarea_counts_in_data_struct(processed_data= processed_data_list, dimension_name= dimension_name,
                                                              textarea_input_counts= textarea_input_counts)
                textarea_input_counts = 0

                dimension_name = response_value
                data_struct = {'dimension_name': dimension_name,
                               'responses': {}}
                processed_data_list.append(data_struct)

                continue

            if type_response == 'TEXTAREA':
                textarea_input_counts += 1

            if (type_response == 'CHECKBOXES') and ('options' not in data):
                continue

            if isinstance(response_value, list): 
                response_value = self.__extract_selected_response_value_text(options= data.get('options'), id= response_value[0])

            self.__add_response_data_in_data_struct(processed_data= processed_data_list, dimension_name= dimension_name,
                                            response_label= response_label, response_value= response_value)
            
        logger.info("Todos os dados das dimensões do formulário foram estruturados com sucesso!")
            
        return processed_data_list
    
    @classmethod
    def __extract_user_data(cls, dimension_data: List[Dict]) -> Dict:
        for data in dimension_data:
            if data['dimension_name'] == "Identificação do Usuário":
                responses = data['responses']

                user_data = {
                    "responsible": responses.get('Nome Completo', None),
                    "email": responses.get('E-mail', None),
                    "phone": responses.get('Telefone', None),
                    "business_name": responses.get('Nome do Negócio', None),
                    "sector": responses.get('Área de Atuação', None),
                    "business_description": responses.get('Descrição do Negócio', None),
                    "num_employees": responses.get('Número de Colaboradores', None),
                    "monthly_billing": responses.get('Faturamento Médio Mensal', None)
                }

                logger.info("Os dados de identificação do usuário foram estruturados com sucesso!")

                return user_data
        
        message = 'O bloco dos dados de identificação do usuário não foi encontrado.'
        logger.error(message)
        raise HttpBadRequestError(message)
    
    @classmethod
    def __extract_feedback_data(cls, dimension_data: List[Dict]) -> Dict:
        for data in dimension_data:
            if data['dimension_name'] == "Feedback":
                responses = data['responses']

                feedback_data = {
                    "feedback_score": int(responses.get('Nota de Satisfação', None)),
                    "feedback_comment": responses.get('Sugestão de Melhoria', None),
                }

                logger.info("Os dados de feedback sobre o formulário foram estruturados com sucesso!")

                return feedback_data
    
        message = 'O bloco dos dados de feedback do usuário não foi encontrado.'
        logger.error(message)
        raise HttpBadRequestError(message)