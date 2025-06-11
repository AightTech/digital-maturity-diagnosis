class LLModelInvalidError(Exception):
    def __init__(self, message: str, status_code: int = 501):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.name = 'LLModelInvalid'