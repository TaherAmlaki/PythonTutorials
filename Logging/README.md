## Logging In Python Applications


### Basic Configuration
I have a small code to show how to configure a basic logging.
I show how to log to a file, set log level, and how to format your 
log messages.

### Basic Logging Problems
Here I show what happens if basicConfig is used throughout a large application. 
The behavior of logging can become unpredictable and might create coupling between 
different parts of the application which is not desirable and hard to detect. 

### Advanced Logging For Large Applications
This section provides a standard logging approach in Python. We learn about logger
instances and how to configure and use them to make independent logging functionality
and remove any unnecessary dependency between classes. 

### Rotating Logging
I show how to rotate logs files, based on the size of the log files 
or based on time intervals. 