from typing import Dict, List
import plotly.graph_objects as go
from uuid import uuid4


class RadarPlotGenerator:
    def __init__(self, temp_folder_path: str):
        self.temp_folder_path = temp_folder_path

    def generate(self, maturity_scores: Dict) -> str:
        del maturity_scores['Índice Geral']

        categories = list(maturity_scores.keys())
        values = list(maturity_scores.values())

        categories += [categories[0]]
        values += [values[0]]

        margin = dict(l= 0, r= 0, t= 20, b= 0)

        if len(categories) == 6:
            margin = dict(l= 0, r= 0, t= 20, b= 20)

        fig = self.__set_plot_layout(values= values, categories= categories, margin= margin)

        file_name = f'radar_plot_{uuid4().hex}.png'
        file_path = self.temp_folder_path + file_name

        fig.write_image(file_path)

        return file_path


    @classmethod
    def __set_plot_layout(cls, values: List, categories: List, margin: Dict):
        fig = go.Figure(
                data= go.Scatterpolar(
                    r= values,
                    theta= categories,
                    fill= 'toself',
                    line_color= "#15144d"
                )
            )
        
        fig.update_layout(
                width= 630,
                height= 300,
                margin= margin,
                polar= dict(
                    gridshape= 'linear',
                    bgcolor= 'rgba(0,0,0,0)',
                    radialaxis=dict(
                        visible=True,
                        linecolor= 'black',
                        gridcolor= 'black',
                        range= [0, 100],
                        tickvals= [20, 40, 60, 80, 100],
                        ticktext= ['0.2', '0.4', '0.6', '0.8', ''],
                        tickfont= dict(size= 8, color="#57575B"),
                        tickangle= 0,
                        angle= 0
                    ),
                    angularaxis=dict(
                        tickfont=dict(size= 12, color= '#090626'),
                        rotation= 90, 
                        direction= "clockwise",
                        linecolor= 'black',
                        gridcolor= 'black'
                    )
                ),
                showlegend= False,
                paper_bgcolor= 'rgba(0,0,0,0)',
                plot_bgcolor= 'rgba(0,0,0,0)'
            )

        return fig