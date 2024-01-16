"""This example uses the RadMachine API to fetch the most recent results of a
specific test list on one unit.  It then creates a two column csv file
(session_results.csv) containing with one column being the date the test list was
performed and the second column being the link to the session."""

from requests import Session

# Set your API token and customer identifier here.  As a reminder if you access
# RadMachine at e.g.  https://radmachine.radformation.com/myclinic/ then your
# customer id is "myclinic"
token = "your-api-token-goes-here"
customer_id = "your-customer-id"

# You can set the name of the unit and test you want to download results for
unit_name = "TrueBeam 1"
test_list_name = "Your Test List Name"

url = f"https://radmachine.radformation.com/{customer_id}/api/qa/testlistinstances/"
s = Session()
s.headers['RadAuthorization'] = f"Token {token}"

filters = {
    'unit_test_collection__unit__name': unit_name, # filter results to a specific unit
    'unit_test_collection__test_list__name': test_list_name, # filter results to a specific test list
    'ordering': '-work_completed',  # order with most recent results first
    'limit': 10,  # number of results
    'offset': 0,  # first page
}

response = s.get(url, params=filters)

with open("session_results.csv", "w") as f:
    for result in response.json()['results']:
        date = result['work_completed']
        url = result['site_url']
        f.write(f"{date},{url}\n")
