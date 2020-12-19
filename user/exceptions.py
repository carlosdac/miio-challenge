from rest_framework.exceptions import APIException



class NonAuthorized(APIException):
  status_code = 401
  def __init__(self, description="You are not authenticated."):
    self.default_detail = description
    self.default_code = 'non_authorized'
    self.detail = self.default_detail