class FileNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.name = 'FileNotFound'
        self.status_code = 404