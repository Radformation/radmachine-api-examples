"""This example uses the RadMachine API to fetch all of the recent results of a
specific test on one unit.  It then creates a two column csv file
(all_test_results.csv) containing with one column being the date the test was
performed and the second column being the result value."""

import time
from requests import Session

# Set your API token and customer identifier here.  As a reminder if you access
# RadMachine at e.g.  https://radmachine.radformation.com/myclinic/ then your
# customer id is "myclinic"
token = "your-api-token-goes-here"
customer_id = "your-customer-id"

# You can set the name of the unit and test you want to download results for
unit_name = "Example - TrueBeam 1"
test_name = "Measured Dose (cGy) :: 6MV"

s = Session()
s.headers['RadAuthorization'] = f"Token {token}"

filters = {
    'unit_test_info__unit__name': unit_name, # filter results to a specific unit
    'unit_test_info__test__name': test_name, # filter results to a specific test
    'skipped': False,  # ensure the test was not skipped
    'ordering': '-work_completed',  # order with most recent results first
}


with open("all_test_results.csv", "w") as f:

    # url for the first page of results
    next_page = f"https://radmachine.radformation.com/{customer_id}/api/qa/testinstances/"

    while next_page:
        response = s.get(next_page, params=filters)
        payload = response.json()

        # url of the next page of results. If there are no more results
        # next_page will be None and the loop will terminate
        next_page = payload['next']

        for result in payload['results']:
            date = result['work_completed']
            value = result['value']
            f.write(f"{date},{value}\n")

        if next_page:
            # don't make requests too quickly!
            time.sleep(0.5)
