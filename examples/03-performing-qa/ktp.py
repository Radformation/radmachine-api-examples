"""This example uses the RadMachine API to create a QA Session for a simple
test list to calculate a temperature pressure correction.  In order
to test this example out, you will need to create and assign a test list
with three tests:
    1) Temperature API Test: A numerical test with identifier `temperature`
    2) Pressure API Test: A numerical test with identifier `pressure`
    3) T&P correction API Test: A calculation test with identifier `ktp` and
       a calculation procedure of `result = (temperature + 273.15) / 295.15 * 760 / pressure`

You will then need the Assignments ID which you can get from the URL when editing the
assignment or performing the assignment via the Web UI.  For example, if you
are performing the test list in the UI, it will have a url like:
    https://radmachine.radformation.com/<customer_id>/qa/utc/perform/123/
which means your assignment identifier is `123` """

from requests import Session
import random


def get_weather():
    """A mock function to simulate getting atmospheric conditions (e.g. from a
    local weather station"""
    temperature = 22
    pressure = 750
    comment = "Storm coming!"
    return temperature, pressure, comment


token = "your-api-token-goes-here"
customer_id = "your-customer-id"

# set your assignment ID here
assignment_id = "123"

# This is the URL we use to submit our QA data to. TestListInstance is
# synonymous with QA Session.
url = f"https://radmachine.radformation.com/{customer_id}/api/qa/testlistinstances/"

# This is the URL we use to tell RadMachine which Assignment we are performing.
# UnitTestCollection is synonymous with Assignment
assignment_url = f"https://radmachine.radformation.com/{customer_id}/api/qa/unittestcollections/{assignment_id}/"

s = Session()
s.headers['RadAuthorization'] = f"Token {token}"

# get the atmospheric conditions
temperature, pressure, comment = get_weather()

# the payload that will be converted to JSON to post to the RadMachine API.
# Note that we don't need to include an entry in the `tests` field for the
# calculated ktp field.
data = {
    'unit_test_collection': assignment_url,
    'work_started': "2023-04-12 10:00",
    'work_completed': "2023-04-12 10:01",
    'tests': {
        "temperature": {"value": temperature},
        "pressure": {"value": pressure},
    },
    'comment': comment,
}

# note we use the POST HTTP method when performing QA
response = s.post(url, json=data)

# checking the status code to ensure our post succeeded
if response.status_code == 201:
    # this will print out the URL you can use to view your results on the site
    print("Success!")
    print(response.json()['site_url'])
else:
    print("The request failed")
    print(response.json())
