import datetime
from typing import Dict, Any


# TODO переписать эту байду
class BaseAuthPayload:

    def __init__(self, service: Dict[str, str]):
        self.service = service

    def create_payload(self, user: Dict[str, str], **kw: Dict[str, str]) -> Dict[str, Any]:

        payload = {
            'login': user['login'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.service['jwt_ttl_minutes']),
        }

        return payload


class Admin(BaseAuthPayload):

    def create_payload(self, user: Dict[str, str], **kw: Dict[str, str]) -> Dict[str, Any]:

        payload = {
            'login': user['login'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.service['jwt_ttl_minutes']),
            'is_admin': True
        }

        return payload


class BeerBlog(BaseAuthPayload):

    def create_payload(self, user: Dict[str, str], **kw: Dict[str, str]) -> Dict[str, Any]:

        payload = {
            'login': user['login'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.service['jwt_ttl_minutes']),
            'is_admin': True,
            'section': kw['section']
        }

        return payload
