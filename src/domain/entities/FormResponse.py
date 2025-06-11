from typing import List, Dict

class FormResponse:
    def __init__(self, dimensions_data: List[Dict], user_data: Dict, feedback_data: Dict):
        self.dimensions_data = dimensions_data
        self.user_data = user_data
        self.feedback_data = feedback_data
        self.__clean_collaborators_dimension_when_none_exists()
    
    
    def __clean_collaborators_dimension_when_none_exists(self):
        num_employees = self.user_data['num_employees']
        if num_employees == 0:
            for data in self.dimensions_data:
                if data['dimension_name'] == "Domínio dos Colaboradores":
                    data['responses'] = []