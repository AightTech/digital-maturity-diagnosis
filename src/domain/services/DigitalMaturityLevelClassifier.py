from typing import Dict

class DigitalMaturityClassesClassifier:
    @classmethod
    def classify(cls, dimension_maturity_scores: Dict) -> Dict:
        dimension_maturity_cls = {}

        for dimension_name, score in dimension_maturity_scores.items():
            if score == 0:
                level = 'Não possui nível'
            elif score <= 25:
                level = 'Iniciante'
            elif score <= 50:
                level = 'Emergente'
            elif score <= 70:
                level = 'Estável'
            elif score <= 90:
                level = 'Avançado'
            else:
                level = 'Otimizado'
            
            dimension_maturity_cls[dimension_name] = level

        return dimension_maturity_cls