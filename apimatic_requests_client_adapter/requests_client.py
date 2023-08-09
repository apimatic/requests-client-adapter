# -*- coding: utf-8 -*-
from requests.packages import urllib3
from cachecontrol import CacheControl
from apimatic_core_interfaces.client.http_client import HttpClient
from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum
from requests import session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RequestsClient(HttpClient):
    """An implementation of CoreHttpClient that uses Requests as its HTTP Client

    Attributes:
        timeout (int): The default timeout for all API requests.

    """

    def __init__(self,
                 timeout=60,
                 cache=False,
                 max_retries=None,
                 backoff_factor=None,
                 retry_statuses=None,
                 retry_methods=None,
                 verify=True,
                 http_client_instance=None,
                 override_http_client_configuration=False,
                 response_factory=None):
        """The constructor.

        Args:
            timeout (float): The default global timeout(seconds).

        """
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if http_client_instance is None:
            self.create_default_http_client(timeout, cache, max_retries,
                                            backoff_factor, retry_statuses,
                                            retry_methods, verify)
        else:
            if override_http_client_configuration:
                http_client_instance.timeout = timeout
                if hasattr(http_client_instance, 'session'):
                    http_client_instance.session.verify = verify
                adapters = http_client_instance.session.adapters
                for adapter in adapters.values():
                    adapter.max_retries.total = max_retries
                    adapter.max_retries.backoff_factor = backoff_factor
                    adapter.max_retries.status_forcelist = retry_statuses
                    adapter.max_retries.allowed_methods = retry_methods

            self.timeout = http_client_instance.timeout
            if hasattr(http_client_instance, 'session'):
                self.session = http_client_instance.session
        self.response_factory = response_factory

    def create_default_http_client(self,
                                   timeout=60,
                                   cache=False,
                                   max_retries=None,
                                   backoff_factor=None,
                                   retry_statuses=None,
                                   retry_methods=None,
                                   verify=True):
        self.timeout = timeout
        self.session = session()

        retries = Retry(total=max_retries, backoff_factor=backoff_factor,
                        status_forcelist=retry_statuses, allowed_methods=retry_methods)
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        if cache:
            self.session = CacheControl(self.session)

        self.session.verify = verify

    def force_retries(self, request, should_retry=None):
        """Reset retries according to each request

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            should_retry (boolean): whether to retry on a particular request

        """
        adapters = self.session.adapters
        if should_retry is False:
            for adapter in adapters.values():
                adapter.max_retries = False
        elif should_retry is True:
            for adapter in adapters.values():
                adapter.max_retries.allowed_methods = [request.http_method]

    def execute(self, request, endpoint_configuration):
        """Execute a given HttpRequest to get a string response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            endpoint_configuration (EndpointConfiguration): The endpoint configurations to use.

        Returns:
            CoreHttpResponse: The response of the HttpRequest.

        """

        old_adapters = self.session.adapters
        self.force_retries(request, endpoint_configuration.should_retry)
        response = self.session.request(
            HttpMethodEnum.to_string(request.http_method),
            request.query_url,
            headers=request.headers,
            params=request.query_parameters,
            data=request.parameters,
            files=request.files,
            timeout=self.timeout
        )

        self.session.adapters = old_adapters
        return self.convert_response(response, endpoint_configuration.contains_binary_response, request)

    def convert_response(self, response, contains_binary_response, http_request):
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

        return self.response_factory.create(
            response.status_code,
            response.reason,
            response.headers,
            response_body,
            http_request
        )
