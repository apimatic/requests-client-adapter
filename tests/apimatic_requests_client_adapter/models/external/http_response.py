# -*- coding: utf-8 -*-
from requests.structures import CaseInsensitiveDict


class HttpResponse(object):

    def __init__(self,
                 status_code: int,
                 reason: str,
                 headers: CaseInsensitiveDict,
                 text: str,
                 content: bytes):
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self.text = text
        self.content = content
