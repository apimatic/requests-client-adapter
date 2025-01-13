# -*- coding: utf-8 -*-
import urllib3
from apimatic_core_interfaces.configuration.endpoint_configuration import EndpointConfiguration
from apimatic_core_interfaces.http.http_request import HttpRequest
from apimatic_core_interfaces.http.http_response import HttpResponse
from pydantic import validate_call
from cachecontrol import CacheControl
from apimatic_core_interfaces.http.http_client import HttpClient
from apimatic_core_interfaces.http.http_method_enum import HttpMethodEnum
from requests import session, Session, Response
from requests.adapters import HTTPAdapter
from typing import Optional, List, MutableMapping

from urllib3.util.retry import Retry


class RequestsClient(HttpClient):
    """An implementation of CoreHttpClient that uses Requests as its HTTP Client

    Attributes:
        timeout (int): The default timeout for all API requests.

    """
    session: Session
    timeout: int

    @validate_call(config={"arbitrary_types_allowed": True})
    def __init__(self,
                 timeout: int=60,
                 cache: bool=False,
                 max_retries: int=0,
                 backoff_factor: float=0,
                 retry_statuses: Optional[List[int]]=None,
                 retry_methods: Optional[List[str]]=None,
                 verify: bool=True,
                 http_client_instance: Optional[Session]=None,
                 override_http_client_configuration: bool=False):
        """The constructor.

        Args:
            timeout (float): The default global timeout(seconds).
            cache (bool): Flag to enable/disable cache in the http client.
            max_retries (int): Total number of retries to allow.
            backoff_factor (float): A backoff factor to apply between attempts after the second try.
            retry_statuses (iterable): A set of integer HTTP status codes that we should force a retry on.
            retry_methods (iterable): Set of HTTP method verbs that we should retry on.
            verify (bool): Flag to enable/disable verification of SSL certificate on the host.
            http_client_instance (HttpClient): The custom HTTP client instance to use.
            override_http_client_configuration (bool): Flag to override configuration for the custom HTTP client.
            response_factory (ResponseFactory): The response factory to convert actual server response to SDK response.

        """
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if http_client_instance is None:
            self.create_default_http_client(timeout, cache, max_retries,
                                            backoff_factor, retry_statuses,
                                            retry_methods, verify)
        else:
            self.timeout = timeout
            self.session = http_client_instance
            if override_http_client_configuration:
                self.session.verify = verify
                self.update_retry_strategy(self.session, max_retries, backoff_factor,
                                           retry_statuses, retry_methods)

    @validate_call
    def create_default_http_client(self,
                                   timeout: int=60,
                                   cache: bool=False,
                                   max_retries: Optional[int]=0,
                                   backoff_factor: float=0,
                                   retry_statuses: Optional[List[int]]=None,
                                   retry_methods: Optional[List[str]]=None,
                                   verify: bool=True) -> None:
        """creates the default instance of HTTP client.

        Args:
            timeout (float): The default global timeout(seconds).
            cache (bool): Flag to enable/disable cache in the http client.
            max_retries (int): Total number of retries to allow.
            backoff_factor (float): A backoff factor to apply between attempts after the second try.
            retry_statuses (iterable): A set of integer HTTP status codes that we should force a retry on.
            retry_methods (iterable): Set of HTTP method verbs that we should retry on.
            verify (bool): Flag to enable/disable verification of SSL certificate on the host.

        """
        self.timeout = timeout
        self.session = session()

        if cache:
            self.session = CacheControl(self.session)

        retries: Retry = Retry(total=max_retries, backoff_factor=backoff_factor, status_forcelist=retry_statuses,
                               allowed_methods=retry_methods, raise_on_status=False, raise_on_redirect=False)
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        self.session.verify = verify

    @validate_call
    def force_retries(self, request: HttpRequest, should_retry: Optional[bool]=None) -> None:
        """Reset retries according to each request

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            should_retry (boolean): whether to retry on a particular request

        """
        adapters: MutableMapping = self.session.adapters
        if should_retry is False:
            for adapter in adapters.values():
                adapter.max_retries = False
        elif should_retry is True:
            for adapter in adapters.values():
                adapter.max_retries.allowed_methods = [request.http_method]

    @validate_call
    def execute(self, request: HttpRequest,
                endpoint_configuration: EndpointConfiguration) -> HttpResponse:
        """Execute a given HttpRequest to get a string response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            endpoint_configuration (EndpointConfiguration): The endpoint configurations to use.

        Returns:
            CoreHttpResponse: The response of the HttpRequest.

        """

        old_adapters: MutableMapping = self.session.adapters
        self.force_retries(request, endpoint_configuration.should_retry)
        response: Response = self.session.request(
            HttpMethodEnum.to_string(request.http_method),
            request.query_url,
            headers=request.headers,
            params=request.query_parameters,
            data=request.parameters,
            files=request.files,
            timeout=self.timeout
        )

        self.session.adapters = old_adapters
        return self.convert_response(response, endpoint_configuration.has_binary_response, request)

    @validate_call(config={"arbitrary_types_allowed": True})
    def convert_response(self, response: Response, contains_binary_response: bool,
                         http_request: HttpRequest) -> HttpResponse:
        """Converts the Response object of the CoreHttpClient into an
        CoreHttpResponse object.

        Args:
            response (dynamic): The original response object.
            contains_binary_response (bool): The flag to check if the response is of binary type.
            http_request (HttpRequest): The original HttpRequest object.

        Returns:
            CoreHttpResponse: The converted CoreHttpResponse object.

        """
        response_body = response.content if contains_binary_response else response.text

        return HttpResponse(
            status_code=response.status_code,
            reason_phrase=response.reason,
            headers={**response.headers},
            text=response_body,
            request=http_request
        )

    @staticmethod
    @validate_call(config={"arbitrary_types_allowed": True})
    def update_retry_strategy(custom_session: Session,
                              max_retries: Optional[int]=None,
                              backoff_factor: Optional[float]=None,
                              retry_statuses: Optional[List[int]]=None,
                              retry_methods: Optional[List[str]]=None):
        """Updates the retry strategy for the provided http client instance

        Args:
            custom_session (Session): The session of the http client instance to update.
            max_retries (int): Total number of retries to allow.
            backoff_factor (float): A backoff factor to apply between attempts after the second try.
            retry_statuses (iterable): A set of integer HTTP status codes that we should force a retry on.
            retry_methods (iterable): Set of HTTP method verbs that we should retry on.
        """
        adapters: MutableMapping = custom_session.adapters
        for adapter in adapters.values():
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'total'):
                adapter.max_retries.total = max_retries
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'backoff_factor'):
                adapter.max_retries.backoff_factor = backoff_factor
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'status_forcelist'):
                adapter.max_retries.status_forcelist = retry_statuses
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'allowed_methods'):
                adapter.max_retries.allowed_methods = retry_methods
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'raise_on_status'):
                adapter.max_retries.raise_on_status = False
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'raise_on_redirect'):
                adapter.max_retries.raise_on_redirect = False
