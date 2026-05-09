from fastapi import HTTPException, status


class EmailException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)
