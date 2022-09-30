# apimatic-requests-client-adapter

Requests is a simple, yet elegant, HTTP library.
This repository contains the client implementation that uses the requests library for APIMatics python SDK. 

## Version supported 
Currenty APIMatic supports  `Python version 3.7 - 3.9`  hence the request-client-lib will need the same versions to be supported

## Installation 
Simply run the command below in you SDK as the requests-client-lib has been added as a dependency in the SDK
```python
pip install -r requirements.txt
```
**Supported Methods Provided by requests-client**

| Method                           | Description                                                                                                          |
| ---------------------------------|----------------------------------------------------------------------------------------------------------------------|
| [`create_default_http_client`](core_http_client/requests_client.py) | function to creat a defaultp http client                                          | 
| [`force_retries`](core_http_client/requests_client.py)              | Reset retries according to each request                                           | 
| [`execute`](core_http_client/requests_client.py)                    | Execute a given HttpRequest to get a string response back                         | 
| [`convert_response`](core_http_client/requests_client.py)           |Converts the Response object of the CoreHttpClient into an CoreHttpResponse object |

## Tests
The requests client implementation also contains unit tests to ensure reliability of the implementation and to prevent unwanted breakages.

## Links
* [apimatic-core-interfaces](https://github.com/apimatic/core-interfaces-python)
* [Requests](https://pypi.org/project/requests/)
