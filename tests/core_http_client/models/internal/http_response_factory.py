from core_interfaces.factories.response_factory import ResponseFactory

from tests.core_http_client.models.internal.http_response import HttpResponse


class HttpResponseFactory(ResponseFactory):

    def __init__(self):
        pass

    def create(self, status_code, reason_phrase, headers, body, request):
        return HttpResponse(status_code, reason_phrase, headers, body, request)
