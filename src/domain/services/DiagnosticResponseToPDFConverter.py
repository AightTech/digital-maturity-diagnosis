from typing import Dict, List
from fpdf import FPDF
from PIL import Image
from math import ceil
from datetime import datetime
from src.config.logger_config import setup_logger

logger = setup_logger(name= "DiagnosticResponseToPDFConverter")

class DiagnosticResponseToPDFConverter(FPDF):
    def __init__(self, temp_folder_path: str):
        super().__init__()

        self.temp_folder_path = temp_folder_path

        self.title_char_spacing = -1.5
        self.text_char_spacing = -0.8
        self.pt_to_mm_const = 2.8346

        self.set_page_background('src/img/Aight - Papel Timbrado.png')
        self.set_margins(top= 75, left= 20, right= 20)
        self.set_auto_page_break(auto=True, margin= 30)
        self.add_font("DejaVu", "", "src/fonts/DejaVuSans.ttf")
        self.add_font("Inter", "", "src/fonts/Inter-Regular.ttf")
        self.add_font("Inter", "B", "src/fonts/Inter-Bold.ttf")
        self.add_page()

    def convert(self, diagnostic_response: Dict, maturity_scores: Dict, 
                 maturity_levels: Dict, radar_plot_file_path: str) -> str:
        self.__add_title_page()

        user_info = diagnostic_response['user_info']
        user_info_translated = {
            "Empresa": user_info['company_name'],
            "Responsável": user_info['responsible_name'],
            "Setor": user_info['sector']
        }
        self.__add_client_info(user_info= user_info_translated)

        overview_text = diagnostic_response['overview']
        self.__add_overview(overview_text= overview_text)

        dimension_analysis = diagnostic_response['dimension_analysis']
        self.__add_dimension_analysis(dimension_analysis= dimension_analysis,
                                      maturity_levels= maturity_levels,
                                      maturity_scores= maturity_scores)

        conclusion_text = diagnostic_response['final_conclusion']
        self.___add_final_conclusion(conclusion_text= conclusion_text)

        self.__add_radar_plot(radar_plot_file_path)

        self.__add_diagnostic_method_link()

        company_name = user_info_translated['Empresa'].replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_name = f'DMD_{company_name}_{timestamp}.pdf'
        pdf_path = self.temp_folder_path + pdf_name

        self.output(pdf_path)

        logger.info("O diagnóstico em PDF foi criado com sucesso!")
        
        return pdf_name, pdf_path


    def __add_title_page(self) -> None:
        self.set_font("Inter", "B", 26)
        self.set_char_spacing(self.title_char_spacing)
        self.cell(0, 0, "Diagnóstico de Maturidade Digital", align='C')
        self.ln(15)


    def __add_client_info(self, user_info: Dict) -> None:
        self.set_char_spacing(self.text_char_spacing)
        for key, value in user_info.items():
            self.set_font("DejaVu", "", 12)
            self.cell(self.get_string_width("•  "), 0, f"•  ")
            self.set_font("Inter", "B", 12)
            self.cell(self.get_string_width(f"{key}"), 0, f"{key}")
            self.set_font("Inter", "", 12)
            self.cell(0, 0, f": {value}")
            self.ln(5)
        self.ln(5)


    def __add_overview(self, overview_text: str) -> None:
        self.set_font("Inter", "", 12)
        self.multi_cell(0, 5, overview_text, markdown= True)
        self.ln(10)


    def __add_dimension_analysis(self, dimension_analysis: List, maturity_levels: Dict, maturity_scores: Dict) -> None:
        self.set_char_spacing(self.title_char_spacing)
        self.set_font("Inter", "B", 20)
        self.cell(0, 0, "Análise de Dimensões")
        self.ln(10)
        for dimension in dimension_analysis:
            dimension_name = dimension['dimension_name']
            full_text = dimension['analysis_text']

            title_font_size_pt = 16
            title_height = ceil(title_font_size_pt / self.pt_to_mm_const)  # converte pt para mm
            line_height = 5
            spacing = 8

            # Estimar altura do parágrafo
            self.set_font("Inter", "", 12)
            self.set_char_spacing(self.text_char_spacing)
            lines = self.multi_cell(0, line_height, full_text, split_only=True) # Apenas calcula a quantidade de linhas.
            text_height = len(lines) * line_height

            total_height = title_height + line_height + text_height + spacing

            # Verificar espaço restante
            if self.get_y() + total_height > self.h - self.b_margin:
                self.add_page()

            dimension_cls_title = f"{maturity_levels[dimension_name]} ({maturity_scores[dimension_name]}%)"
            # Renderizar título e parágrafo
            self.set_char_spacing(self.title_char_spacing)
            self.set_font("Inter", "B", title_font_size_pt)
            self.cell(self.get_string_width(dimension_name), 0, dimension_name)
            self.set_font("DejaVu", "", title_font_size_pt)
            self.cell(self.get_string_width(" — "), 0, " — ")
            self.set_font("Inter", "", title_font_size_pt)
            self.cell(0, 0, dimension_cls_title)
            self.ln(line_height)

            self.set_char_spacing(self.text_char_spacing)
            self.set_font("Inter", "", 12)
            self.multi_cell(0, line_height, full_text, markdown=True)
            self.ln(spacing)
        self.ln(3)


    def ___add_final_conclusion(self, conclusion_text: str) -> None:
        title_font_size_pt = 18
        title_height = ceil(title_font_size_pt / self.pt_to_mm_const)  # converte pt para mm
        line_height = 5
        spacing = 10

        # Estimar altura do parágrafo
        self.set_font("Inter", "", 12)
        self.set_char_spacing(self.text_char_spacing)
        lines = self.multi_cell(0, line_height, conclusion_text, split_only=True)  # Apenas calcula a quantidade de linhas.
        text_height = len(lines) * line_height

        total_height = title_height + spacing + text_height

        # Verificar espaço restante
        if self.get_y() + total_height > self.h - self.b_margin:
            self.add_page()

        self.set_char_spacing(self.title_char_spacing)
        self.set_font("Inter", "B", title_font_size_pt)
        self.cell(0, title_height, "Conclusão Final", align='C')
        self.ln(spacing)
        self.set_char_spacing(self.text_char_spacing)
        self.set_font("Inter", "", 12)
        self.multi_cell(0, line_height, conclusion_text, markdown= True)
        self.ln(8)

    @staticmethod
    def __px_to_mm(pixels, dpi= 96) -> float:
        return pixels * 25.4 / dpi

    def __add_radar_plot(self, radar_plot_file_path: str) -> None:
        with Image.open(radar_plot_file_path) as img:
            px_width, px_height = img.size

        image_width = self.__px_to_mm(px_width)
        image_height = self.__px_to_mm(px_height)

        # Se não couber na página, adiciona nova
        if self.get_y() + image_height > self.h - self.b_margin:
            self.add_page()

        self.image(radar_plot_file_path, x= 20, y= self.get_y(), w= image_width)
        self.set_y(self.get_y() + image_height)


    def __add_diagnostic_method_link(self) -> None:
        title = """Quer entender melhor como funciona a nossa avaliação de maturidade digital para o seu negócio?"""
        material_link_text = """material explicativo"""
        material_link = "https://profuse-tithonia-50b.notion.site/Como-funciona-o-m-todo-de-avalia-o-do-Diagn-stico-de-Maturidade-Digital-da-Aight-20648875b70d809399c0e6c969a9c0ce"
        email_link_text = """Ou, entre em contato com a gente através do e-mail: """
        email_link_label = "fala@aight.com.br"
        email_link = "mailto:fala@aight.com.br"
        

        title_font_size_pt = 18
        title_height_line = ceil(title_font_size_pt / self.pt_to_mm_const)  # converte pt para mm

        self.set_font("Inter", "B", title_font_size_pt)
        self.set_char_spacing(self.title_char_spacing)
        n_title_lines = self.multi_cell(0, title_height_line, title, align='C', split_only=True)  # Apenas calcula a quantidade de linhas.
        title_height = len(n_title_lines) * title_height_line

        text_font_size_pt = 12
        text_height_line = ceil(text_font_size_pt / self.pt_to_mm_const)

        text_height = 2 * text_height_line

        spacing = text_height_line

        total_block_height = (title_height + spacing + text_height) + (2 * spacing)

        # Verificar espaço restante
        page_height = self.h
        bottom_margin = self.b_margin

        if self.get_y() + total_block_height > page_height - bottom_margin:
            self.add_page()

            page_height = self.h
            bottom_margin = self.b_margin

        # Posicionar o bloco na parte inferior da página
        self.set_y(page_height - bottom_margin - total_block_height)

        # Imprimir bloco 
        self.set_char_spacing(self.title_char_spacing)
        self.set_font("Inter", "B", title_font_size_pt)
        self.multi_cell(0, title_height_line, title, align= "C")
        self.ln(spacing)

        self.set_char_spacing(self.text_char_spacing)
        self.set_font("DejaVu", "", 12)
        self.cell(self.get_string_width("•  "), text_height_line, f"•  ")
        self.set_font("Inter", "", text_font_size_pt)
        self.cell(self.get_string_width("Acesse o nosso "), text_height_line, "Acesse o nosso ")
        self.set_font("Inter", "B", text_font_size_pt)
        self.set_text_color(0, 0, 139)
        self.cell(self.get_string_width(material_link_text), text_height_line, material_link_text, link= material_link)
        self.set_font("Inter", "", text_font_size_pt)
        self.set_text_color(0, 0, 0)
        self.cell(0, text_height_line, " sobre a metodologia utilizada neste diagnóstico.")
        self.ln(text_height_line)
        self.set_font("DejaVu", "", 12)
        self.cell(self.get_string_width("•  "), text_height_line, f"•  ")
        self.set_font("Inter", "", text_font_size_pt)
        self.cell(self.get_string_width(email_link_text), text_height_line,email_link_text)
        self.set_font("Inter", "B", text_font_size_pt)
        self.set_text_color(0, 0, 139)
        self.cell(0, text_height_line, email_link_label, link= email_link)