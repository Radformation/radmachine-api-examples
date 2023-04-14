"""This example uses the RadMachine API to fetch a list of units from your
RadMachine instance and then prints out the name of each unit found"""

from requests import Session

# Set your API token and customer identifier here.  As a reminder if you access
# RadMachine at e.g.  https://radmachine.radformation.com/myclinic/ then your
# customer id is "myclinic"
token = "your-api-token-goes-here"
customer_id = "your-customer-id"

url = f"https://radmachine.radformation.com/{customer_id}/api/units/units/"
s = Session()
s.headers['RadAuthorization'] = f"Token {token}"

# fetch the units from the RadMachine API
response = s.get(url)

# print the status code of the request.
# 200 means it was successful
# 4XX means there was a problem with your request.  Check that your
# token and customer ID are correct
print("Status code is:", response.status_code)
for unit in response.json()['results']:
    print(unit['name'])
