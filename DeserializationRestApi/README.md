## Deserialization And Serialization In Python

In this tutorial I am looking into methods of handling Json responses and requests from/to 
a Rest Api.

### Marshmallow
Marshmallow is a Python library to convert data between generic complex data types 
and Python's native or custom objects. I show how to create a simple schema for a Python data object 
(custom class) and also a more complex nested schema as well for multi-layered data structure.


### Json Schema
Here I show how to use json schema library to validate a response from RESTful Api. 
I also implement a custom converter class to convert raw (validated) json data into a Python 
object where keys of json data are assigned as instance attributes of the object and can be 
iterated through similar to dictionary.  
 