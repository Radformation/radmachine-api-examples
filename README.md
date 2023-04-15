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
language you want to talk to the API!  Virtually all mainstream languages
(Python, Javascript, Matlab, C#, Ruby, R, VB, ...) have the ability to
serialize & deserialize JSON and make HTTP requests.  Python is a relatively
easy language to read so the examples here should be relatively straightforwrad
to convert to whatever language you're most comfortable with!

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
would be `myclinic`.  To generate your API token visit your User Profile page
in RadMachine.

The examples are as follows:

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
