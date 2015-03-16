from rest_framework.exceptions import APIException as BaseAPIException


class CustomAPIException(BaseAPIException):

    def __init__(self, detail=None, status_code=None):
        self.detail = detail or 'Error occured'
        self.status_code = status_code or 400


