from src.domain.entities.FormResponse import FormResponse

class DimensionDataToMarkdownConverter:
    @classmethod
    def convert(cls, form_response: FormResponse) -> str:
        dimensions_data = form_response.dimensions_data
        form_responses_text = ""

        for data in dimensions_data:
            dimension_name = data.get('dimension_name')
            responses_list = data.get('responses', [])

            if dimension_name == "Feedback":
                break

            form_responses_text += f'### {dimension_name}\n'

            if not responses_list:
                form_responses_text += 'O usuário não teve acesso as questões desta dimensão. Desconsidere no diagnóstico.\n\n'
                continue

            for question in responses_list:
                answer  = responses_list.get(question)

                form_responses_text += question + '\n' + "R: " + str(answer) + '\n\n'

        return form_responses_text