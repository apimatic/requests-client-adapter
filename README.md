# requests-client-lib

Requests is a simple, yet elegant, HTTP library.
This repository contains the client implementation that uses the requests library for APIMatics python SDK.

## Introduction
Requests allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your PUT & POST data — but nowadays, just use the json method!

Requests is one of the most downloaded Python packages today, pulling in around 30M downloads / week— according to GitHub, Requests is currently depended upon by 1,000,000+ repositories. You may certainly put your trust in this code.

## Supported Features & Best–Practices
Requests is ready for the demands of building robust and reliable HTTP–speaking applications, for the needs of today.

Keep-Alive & Connection Pooling
International Domains and URLs
Sessions with Cookie Persistence
Browser-style TLS/SSL Verification
Basic & Digest Authentication
Automatic Content Decompression and Decoding
Multi-part File Uploads
SOCKS Proxy Support
Connection Timeouts
Streaming Downloads
Automatic honoring of .netrc

## Version supported 
Currenty APIMatic supports  `Python version 3.7 - 3.9`  hence the request-client-lib will need the same versions to be supported

## Installation 
Simply run the command below in you SDK as the requests-client-lib has been added as a dependency in the SDK
```python
pip install -r requirements.txt
```
**Supported Methods Provided by requests-client**

| Method               | Description                                                                                                                                                                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `create_default_http_client`     | function to creat a defaultp http client                                                                                                                                                     | 
| `force_retries`    | Reset retries according to each request                                                                                                                     | 
| `execute` | Execute a given HttpRequest to get a string response back | 
| `convert_response` |Converts the Response object of the CoreHttpClient into an CoreHttpResponse object.                                                                                                         |

