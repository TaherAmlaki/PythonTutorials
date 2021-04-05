## WireMock Stubbing and Response Templating

Article:
[Mocking APIs with WireMock, Stubbing and Response Templating](https://www.taheramlaki.com/blog/articles/wiremock-stubbing-and-response-templating/)

### How to run WireMock Standalone Server
Arguments needed to run WireMock Standalone with explanation of most common arguments are 
presented in the article. 

### Working with WireMock endpoints and helpers
A Postman collection for using different admin endpoints, and also setting simple and more advanced 
mocked responses is added to the project and discussed in the article.

### WireMock Server by Python, ContextManager and Subprocess
Implementation of ContextManager protocol in Python to start, health check, and 
shutdown WireMock Server. Allows us to use WireMock Server management inside 
a with-block possible and make sure that WireMock Server will be shut down and 
WireMock subprocess will be terminated before completing with-block.

### UnitTests for WireMock Project
Using Python's unittest module created two sets of unit tests, first for testing context manager
and second to test setting mock data into WireMock.

