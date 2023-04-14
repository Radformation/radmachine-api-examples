# RadMachine API Examples

This repository contains a number of examples of using the RadMachine API to
fetch data and perform QA sessions, as originally presented during
Radformation's RadMachine Scripting Webinar.

We hope you find it useful, and if you have other examples you'd like to see,
please file an
[issue](https://github.com/Radformation/radmachine-api-examples/issues) so
we can consider adding it!

## Getting started

All examples should run on any recent Python 3.X version (there is also [one
Javascript example](./examples/01-hello-api/hello.js) which you can run
with [Node JS](https://nodejs.org/en)).  If you don't have Python installed
you can get it here: https://www.python.org/downloads/. Getting started with
Python including how to run these files is outside the scope of this document
but there are many many blog posts, tutorials, and courses available on the
web.  If you get stuck somewhere you can create an [issue in this code
repository](https://github.com/Radformation/radmachine-api-examples/issues) and
we will help you out!

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
