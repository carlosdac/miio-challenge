from rest_framework.exceptions import APIException


class BadRequest(APIException):
  status_code = 400
  def __init__(self, description=""):
    self.default_detail = description
    self.default_code = 'non_authorized'
    self.detail = self.default_detail



class NonAuthorized(APIException):
  status_code = 401
  def __init__(self, description="You are not authenticated."):
    self.default_detail = description
    self.default_code = 'non_authorized'
    self.detail = self.default_detail