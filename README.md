# RadMachine API Examples

This repository contains a number of examples of using the RadMachine API to
fetch data and perform QA sessions, as originally presented during
Radformation's RadMachine Scripting Webinar.

We hope you find it useful, and if you have other examples you'd like to see,
please file an
[issue](https://github.com/Radformation/radmachine-api-examples/issues) so
we can consider adding it!

## Programming Language Choice

The examples here are mostly written in Python, but you can use whatever
language you want to talk to the API.  Virtually all mainstream languages
(Python, Javascript, Matlab, C#, Ruby, R, VB, ...) have the ability to
serialize & deserialize JSON and make HTTP requests.  Python is a relatively
easy language to read so the examples here should be straightforwrad to convert
to whatever language you're most comfortable with.

If you do convert some of the examples to a different language, please consider
forking this repository, adding your example, and making a pull request so we
can add it here!

## Getting started

All examples should run on any recent Python 3.X version (there is also [one
Javascript example](./examples/01-hello-api/hello.js) which you can run
with [Node JS](https://nodejs.org/en)).  If you don't have Python installed
you can get it here: https://www.python.org/downloads/. Getting started with
Python including how to run these files is outside the scope of this document
but there are many many blog posts, tutorials, and courses available on the
web.  If you get stuck somewhere you can create an [issue in this code
repository](https://github.com/Radformation/radmachine-api-examples/issues) and
we will help you out.

All the examples use the popular
[requests](https://requests.readthedocs.io/en/latest/) library for making HTTP
requests to the RadMachine API.  You will need to [install
it](https://requests.readthedocs.io/en/latest/user/install/#install) prior to
running any of these examples.

The examples are all found in the `examples` subdirectory.  Before running any
example file you will need to edit the file to set your API token and customer
identifier. As a reminder, if you access RadMachine at
https://radmachine.radformation.com/myclinic/, then your customer identifier
would be `myclinic`.  To generate your API token visit your User Profile
(`http://radmachine.radformation.com/<customer_id>/accounts/profile/`) page in
RadMachine.

## List of Examples

Please note that for the sake of simplicity most of the examples included here
have eschewed proper error handling.  This is discussed more below in the Best
Practices section.  With that out of the way, the examples are listed below:

* [./examples/01-hello-api/hello.py](./examples/01-hello-api/hello.py)
    * Use the API to fetch a list of all your units and print their names using Python
* [./examples/01-hello-api/hello.js](./examples/01-hello-api/hello.js)
    * Use the API to fetch a list of all your units and print their names using Javascript
* [./examples/02-fetch-test-results/test_results.py](./examples/02-fetch-test-results/test_results.py)
    * Use the API to fetch the most recent results for a specific test performed on a unit.
      Demonstrates filtering and ordering of results
* [./examples/02-fetch-test-results/all_test_results.py](./examples/02-fetch-test-results/all_test_results.py)
    * Use the API to fetch *all* of the results for a specific test performed on a unit
      Demonstrates fetching multiple pages of results
* [./examples/03-performing-qa/ktp.py](./examples/03-performing-qa/ktp.py)
    * Use the API to perform a simple test list with two numerical tests and a calculation.
      Demonstrates basic QA session creation
* [./examples/04-upload-test/upload_text.py](./examples/04-upload-test/upload_text.py)
    * Use the API to perform a test list that requires uploading a text file.
      Demonstrates QA session creation with an upload test
* [./examples/04-upload-test/upload_dicom.py](./examples/04-upload-test/upload_dicom.py)
    * Use the API to perform a test list that requires uploading a dicom file.
      Demonstrates Base 64 encoding a binary file for upload
* [./examples/05-reports/qa_session_report.py](./examples/05-reports/qa_session_report.py)
    * Use the API to download a report for a specific QA Session
* [./examples/05-reports/saved_reports.py](./examples/05-reports/saved_reports.py)
    * Use the API to run all of your saved reports
* [./examples/06-qa-repeater/qa-repeater.py](./examples/06-qa-repeater/qarepeater.py)
    * A QARepeater class that demonstrates how to perform a constancy check using the API


## API Usage Best Practices


### Tokens

Because someone in posession of your API token can take actions on your behalf,
they should be considered sensitive and treated in a manner similar to
passwords.  When possible we recommend creating a specific RadMachine "API User"
with a limited amount of permissions.  RadMachine has two built in User Groups
"API Performer" and "API ReadOnly" which can be useful for this purpose (if
these groups are not present in your instance, please contact support and they
will be happy to add them).

You may revoke your existing token and regenerate a new unique token at any
time by visiting your User Profile page.

### Status codes & Error handling

As mentioned above, most of the included example scripts have intentionally
avoided handling error conditions in favour of brevity & simplicity.  It is
just about guaranteed that when dealing with network requests (and in our
experience, hospital networks in particular!) you will encounter flaky
interent connections, proxy issues, server errors and more.  Given that, if you
are writing a script or application you are going to deploy in the clinic it is
well worth taking the time to consider potential error conditions and handling
them as gracefully as possible

In general you will encounter 4 classes of HTTP response status codes:

* 2XX - Everything went according to plan!
* 3XX - The resource you are trying to reach has been moved
* 4XX - Typically indicates something is wrong with your request
* 5XX - Your request generated an error on the server (often an indication of a bug on our side)

In RadMachine the most common status codes you will encounter are:

* 200 - Your request to fetch some data, or update an existing object, was successful
* 201 - Your request to create a new object on the server (e.g. a QA Session) was successful
* 400 - Usually received when there is a problem with the data in your request to create a new QA session
* 401 - You forgot to include your authentication header or your token was invalid
* 403 - Your user does not have permission to access the resource you are trying to reach
* 500 - Your request generated an error on the server

An example of handling different status codes when attempting to create a QA
session with the RadMachine API might look like:

```
import requests
s = requests.Session()

...

resp = s.post(url, json=data)
if resp.status_code >= 500:
    print("server error. Contact support!")
elif resp.status_code >= 400:
    print("Something wrong with our request.", resp.json())
elif resp.status_code == 201:
    print("QA Session created!", resp.json())
```

### Limit your requests

When dealing with API's it is generally a good idea to be a considerate user by
not flooding the server with requests.  It depends on the API you are dealing
with but generally, inserting a pause of 0.5s - 1s should be adequate. For
example:

```python
    # hammer the server!
    while True: # :(
        response = s.get(url)

    # that's more like it!
    while True: # :)
        response = s.get(url)
        time.sleep(0.5)
```

You should also be conscious of not repeating requests unnecessarily.  Making
use of caches and removing redundant API calls can make your program run faster
and keep the API servers happy. For example:


```python
    tests = ["6MV Output", "10MV Output"]
    units = ["Unit 1", "Unit 2"]

    # test details gest called every loop but never changes :(
    for unit in units:
        test_details = s.get(".../qa/tests/", params={"name__in": tests}) # :(
        unit = s.get(".../units/units/", params={"name": unit})

    # move the redundant call out of the loop
    test_details = s.get(".../qa/tests/", params={"name__in": tests}) # :)
    for unit in units:
        unit = s.get(".../units/units/", params={"name": unit})

```
