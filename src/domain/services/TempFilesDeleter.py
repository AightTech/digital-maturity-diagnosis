from src.errors.types.FileNotFoundException import FileNotFoundException
from src.errors.types.HttpServerError import HttpServerError
from src.config.logger_config import setup_logger
from typing import List
import os

logger = setup_logger(name= "TempFilesDeleter")

class TempFilesDeleter:
    def __init__(self, temp_folder_path: str = 'src/tmp'):
        self.temp_folder_path = temp_folder_path

    def delete(self, file_paths: List[str]) -> None:
        for file_path in file_paths:
            if not os.path.isfile(file_path):
                message = f"O arquivo '{file_path}' não encontrado." 
                logger.warning(message)
                raise FileNotFoundException(message)
            
            try:
                os.remove(file_path)
                logger.info(f"O arquivo '{file_path}' foi removido com sucesso!")

            except Exception as e:
                message = f"Erro ao remover arquivo '{file_path}': {e}"
                logger.error(message)
                raise HttpServerError(message)