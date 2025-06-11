from pydantic import BaseModel
from typing import List

class UserInfo(BaseModel):
    company_name: str
    responsible_name: str
    sector: str

class DimensionAnalysis(BaseModel):
    dimension_name: str
    analysis_text: str

class DiagnosisOutput(BaseModel):
    user_info: UserInfo
    overview: str
    dimension_analysis: List[DimensionAnalysis]
    final_conclusion: str