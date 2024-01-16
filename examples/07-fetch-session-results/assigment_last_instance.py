"""This example uses the RadMachine API to fetch the most recent results of a
specific test on one unit. It is similar to session_results.py except it uses
the unittestcollection endpoints last_instance field to get the results."""

from requests import Session

# Set your API token and customer identifier here.  As a reminder if you access
# RadMachine at e.g.  https://radmachine.radformation.com/myclinic/ then your
# customer id is "myclinic"
token = "your-api-token-goes-here"
customer_id = "your-customer-id"

# You can set the name of the unit and test you want to download results for
unit_name = "TrueBeam 1"
test_list_name = "Your Test List"

url = f"https://radmachine.radformation.com/{customer_id}/api/qa/unittestcollections/"
s = Session()
s.headers['RadAuthorization'] = f"Token {token}"

filters = {
    'unit__name': unit_name, # filter results to a specific unit
    'test_list__name': test_list_name, # filter results to a specific test list
    'ordering': '-work_completed',  # order with most recent results first
    'limit': 1,  # number of results
    'offset': 0,  # first page
}

response = s.get(url, params=filters)
last_instance_url = response.json()['results'][0]['last_instance']
if last_instance_url:
    last_instance_response = s.get(last_instance_url)
    payload = last_instance_response.json()
    print(payload['work_completed'], payload['site_url'])

