# apimatic-requests-client-adapter

Requests is a simple, yet elegant, HTTP library.
This repository contains the client implementation that uses the requests library for APIMatics python SDK. 

## Version supported 
Currenty APIMatic supports  `Python version 3.7 - 3.9`  hence the apimatic-requests-client-adapter will need the same versions to be supported

## Installation 
Simply run the command below in your SDK as the requests-client-lib will be added as a dependency in the SDK
```python
pip install apimatic-requests-client-adapter
```
**Supported Methods Provided by requests-client**

| Method                                                                             | Description                                                                      |
| -----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| [`create_default_http_client`](apimatic_requests_client_adapter/requests_client.py)| function to creat a defaultp http client                                         | 
| [`force_retries`](apimatic_requests_client_adapter/requests_client.py)             | Reset retries according to each request                                          | 
| [`execute`](apimatic_requests_client_adapter/requests_client.py)                   | Execute a given HttpRequest to get a string response back                        | 
| [`convert_response`](apimatic_requests_client_adapter/requests_client.py)          | Converts the Response object of the CoreHttpClient into a CoreHttpResponse object|

## Tests
The requests client implementation also contains unit tests to ensure reliability of the implementation and to prevent unwanted breakages.

## Links
* [apimatic-core-interfaces](https://pypi.org/project/apimatic-core-interfaces/)
* [Requests](https://pypi.org/project/requests/)
