from fastapi import HTTPException, status


class HttpExceptions:

    @staticmethod
    def not_found_exception(msg='Not found'):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

    @staticmethod
    def internal_server_error(msg='Internal server error'):
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

    @staticmethod
    def bad_request_exception(msg='Bad request'):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    @staticmethod
    def invalid_token(msg='Invalid token or expired token was provided'):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

    @staticmethod
    def invalid_credentials(msg='Invalid credentials provided'):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)
