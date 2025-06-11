import re
from typing import Dict
from src.domain.entities.FormResponse import FormResponse

class DigitalMaturityScoresCalculator:
    
    def calculate(self, form_response: FormResponse) -> Dict:
        dimensions_data = form_response.dimensions_data
        dimensions_scores = {}

        for data in dimensions_data:
            dimension_name = data.get('dimension_name')
            responses_list = data.get('responses', [])
            len_responses_list = len(list(responses_list))
            score_sum = 0
            score_max = len_responses_list * 3

            if (dimension_name == "Identificação do Usuário") or (not score_max):
                continue

            if dimension_name == "Feedback":
                break
            
            if data.get('textarea_counts', []):
                score_max = (len_responses_list - int(data.get('textarea_counts'))) * 3

            for question in responses_list:
                answer = responses_list.get(question)
                score = re.match(r"\d+", answer)

                if score:
                    score_sum += int(score.group())

            maturity_score = round((score_sum / score_max) * 100, 2)
            dimensions_scores[dimension_name] = maturity_score

        general_maturity_score = self._generate_overall_maturity_index(dimensions_scores)
        dimensions_scores["Índice Geral"] = general_maturity_score

        return dimensions_scores


    @classmethod
    def _generate_overall_maturity_index(cls, dimensions_scores: Dict) -> float:
        values = [score for score in dimensions_scores.values()]
        
        return round(sum(values) / len(values), 2) if values else 0.0