from apimatic_core_interfaces.http.http_method_enum import HttpMethodEnum
from pydantic import validate_call
from requests import Session, Response
from requests.adapters import HTTPAdapter
from typing import Optional, List, Dict, Union, Any

from requests.structures import CaseInsensitiveDict
from urllib3 import Retry

from apimatic_requests_client_adapter.requests_client import RequestsClient
from apimatic_core_interfaces.http.http_request import HttpRequest
from apimatic_core_interfaces.http.http_response import HttpResponse


class Base:

    @staticmethod
    @validate_call
    def request() -> HttpRequest:
        return HttpRequest(http_method=HttpMethodEnum.GET, query_url='http://localhost:3000/test')

    @staticmethod
    @validate_call
    def response(status_code: int=200, reason_phrase: Optional[str]=None,
                 headers: Optional[Dict[str, str]]=None, text: Optional[Union[str, bytes]]=None) -> HttpResponse:
        return HttpResponse(status_code=status_code, reason_phrase=reason_phrase,
                            headers=headers, text=text, request=Base.request())

    @staticmethod
    @validate_call(config={'arbitrary_types_allowed': True})
    def actual_response_from_client(status_code: int=200, reason: Optional[str]=None,
                                    headers: Optional[CaseInsensitiveDict]=None, text: Optional[str]=None,
                                    content: Union[str, bytes, Any]=None) -> Response:
        response = Response()
        response.status_code = status_code
        response.reason = reason
        response.headers = headers

        # Set encoding if available
        if "Content-Type" in response.headers and "charset=" in response.headers["Content-Type"]:
            response.encoding = response.headers["Content-Type"].split("charset=")[-1]
        else:
            response.encoding = "utf-8"  # Default encoding

        # Populate _content based on text or content
        if text is not None:
            response._content = text.encode(response.encoding)  # Encode text as bytes using the encoding
        elif content is not None:
            response._content = content
        else:
            response._content = b""  # Default to empty bytes if no text or content

        response._content_consumed = True
        return response

    @property
    @validate_call
    def client(self) -> RequestsClient:
        return RequestsClient()

    @staticmethod
    @validate_call
    def create_custom_session(max_retries: Optional[int]=None,
                              backoff_factor: Optional[float]=None,
                              retry_statuses: Optional[List[int]]=None,
                              retry_methods: Optional[List[str]]=None,
                              verify: bool=True) -> Session:
        session = Session()
        retries: Retry = Retry(total=max_retries, backoff_factor=backoff_factor, status_forcelist=retry_statuses,
                               allowed_methods=retry_methods, raise_on_status=False, raise_on_redirect=False)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        session.verify = verify

        return session

    @staticmethod
    @validate_call(config={'arbitrary_types_allowed': True})
    def create_request_client(timeout: int=60,
                              cache: bool=False,
                              max_retries: int=3,
                              backoff_factor: float=0,
                              retry_statuses: Optional[List[int]]=None,
                              retry_methods: Optional[List[str]]=None,
                              verify: bool=True,
                              http_client_instance: Optional[Session]=None,
                              override_http_client_configuration: bool=False) -> RequestsClient:
        return RequestsClient(timeout=timeout, cache=cache, max_retries=max_retries, backoff_factor=backoff_factor,
                              retry_statuses=retry_statuses, retry_methods=retry_methods, verify=verify,
                              http_client_instance=http_client_instance,
                              override_http_client_configuration=override_http_client_configuration)