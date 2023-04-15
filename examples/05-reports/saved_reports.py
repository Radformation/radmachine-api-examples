"""This is example of using the API to run all of your saved reports and save
them to disk."""

from requests import Session
import time

# set your token and customer ID here
token = "your-api-token-goes-here"
customer_id = "your-customer-id"

s = Session()
s.headers['RadAuthorization'] = f"Token {token}"

# first we get a list of all the saved reports we created
filters =  {'created_by__username': 'rtaylor@radformation.com'}
url = f"https://radmachine.radformation.com/{customer_id}/api/reports/savedreports/"
response = s.get(url, params=filters)

# now we loop through the list and run each of the reports
report_params =  {"report_format": "pdf"}
report_list = response.json()['results']
for report in report_list:
    report_url = report['run_report_url']
    print(f"Running report {report['title']}...")
    response = s.get(report_url, params=report_params)
    filename = response.headers['filename']
    with open(filename, 'wb') as f:
        f.write(response.content)
        print(f"\tWrote {f.tell()} bytes to {filename}")

    # sleep for a short period so we limit the rate of our requests
    time.sleep(0.5)
