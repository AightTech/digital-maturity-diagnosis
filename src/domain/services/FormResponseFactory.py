from src.validators.DimensionDataSchemaValidator import DimensionDataSchemaValidator
from src.validators.FeedbackDataSchemaValidator import FeedbackDataSchemaValidator
from src.validators.UserDataSchemaValidator import UserDataSchemaValidator
from src.domain.entities.FormResponse import FormResponse
from typing import Dict, List


class FormResponseFactory:
    def __init__(self):
        self.dimension_data_validator = DimensionDataSchemaValidator()
        self.user_data_validator = UserDataSchemaValidator()
        self.feedback_validator = FeedbackDataSchemaValidator()

    def create(self, dimensions_data: List[Dict], user_data: Dict, feedback_data: Dict) -> FormResponse:
        self.dimension_data_validator.validate(dimension_data= dimensions_data)
        self.user_data_validator.validate(user_data= user_data)
        self.feedback_validator.validate(feedback_data= feedback_data)
        
        return FormResponse(user_data= user_data,
                            dimensions_data= dimensions_data,
                            feedback_data= feedback_data)