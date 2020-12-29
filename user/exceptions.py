from rest_framework.exceptions import APIException

"""
This class implements APIException and is used where a token is sent not or if a owner is tentando updates in
a Regular Plan of he is not owner.
"""
class NonAuthorized(APIException):
  status_code = 401
  def __init__(self, description="Authentication credentials were not provided."):
    self.default_detail = description
    self.default_code = 'non_authorized'
    self.detail = self.default_detail