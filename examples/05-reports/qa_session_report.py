"""This is a simple API example that shows you how to download a PDF report for
a specific QA session.

When you create a QA session via the API, the response you receive back from the
RadMachine server will have a `url` field which you can then easily use to
generate a report for that specific session.  For example:

    test_data = {
      ...
    }
    response = s.post(url, json=test_data)
    if response.status_code == 201:
        # session created!
        session_url = response.json()['url']

        # construct a report url based on the session_url
        report_url = f"{session_url}report/"
        report_resp = s.get(report_url, params={'report_format': 'pdf'})
        with open("report.pdf", 'wb') as f:
            f.write(response.content)

As a simpler demonstration, the example below fetches the most recent QA session from the
API.  You could also directly construct a report url with a known session ID like:

    session_id = 123
    session_url = f"https://radmachine.radformation.com/<customer>/api/qa/testlistinstances/{session_id}"
    report_url = f"{session_url}/report/

"""

from requests import Session


# set your token and customer ID here
token = "your-api-token-goes-here"
customer_id = "your-customer-id"

s = Session()
s.headers['RadAuthorization'] = f"Token {token}"

# QA Sessions list endpoint.  TestListInstance is synonymous with QaSession
sessions_url = f"https://radmachine.radformation.com/{customer_id}/api/qa/testlistinstances/"
params =  {
    'order_by': '-work_completed', # order by date, the '-' prefix means descending or most recent first
    'offset': 0, # we want the first page of results
    'limit': 1,  # and we only need one result
}
response = s.get(sessions_url, params=params)

# Get the details url for the most recent session
latest_session_url = response.json()['results'][0]['url']
# The session report url format is :
#    https://radmachine.radformation.com/{customer_id}/api/qa/testlistinstances/{session_id}/report/
report_url = f"{latest_session_url}report/"

# generate and download the report
report_params = {'report_format': 'pdf'} # pdf, xlsx, or csv
response = s.get(report_url, params=report_params)

# RadMachine returns a filename header which you can use if you like!
filename = response.headers['filename']
with open(filename, 'wb') as f:
    f.write(response.content)
    print(f"Wrote {f.tell()} bytes to {filename}")
