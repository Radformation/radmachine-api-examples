"""This example uses the RadMachine API to create a QA Session for a test
list containg an upload test and two calculations. Because we are uploading
a binary DICOM file, we need to first Base64 encode the file (base 64 allows
us to use a text representation of binary data).

In order to test this example out, you will need to create and assign a test
list with three tests:

    1) DICOM Upload API Test: An upload test with the identifier `dicom_upload`
    and the following code set as the calculation procedure:

        import pydicom
        import matplotlib.pyplot as plt

        dataset = pydicom.read_file(BIN_FILE)

        plt.imshow(dataset.pixel_array)
        UTILS.write_file("dataset.png", plt.gcf())

        result = {
            "gantry": float(dataset.GantryAngle),
            "collimator": float(dataset.BeamLimitingDeviceAngle),
        }

    2) Gantry Angle API Test : A calculation test with identifier `gantry_angle` and
        calculation procedure `result = dicom_upload["gantry"]`
    2) Collimator Angle API Test : A calculation test with identifier `collimator_angle` and
        calculation procedure `result = dicom_upload["collimator"]`

You will then need the Assignments ID which you can get from the URL when
editing the assignment or performing the assignment via the Web UI.  For
example, if you are performing the test list in the UI, it will have a url
like:
    https://radmachine.radformation.com/<customer_id>/qa/utc/perform/123/
which means your assignment identifier is `123` """

from requests import Session
import base64
import random


# set your token and customer ID here
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

# read and encode our binary data as b64 text
f = open("test.dcm", "rb")
b64_encoded = base64.b64encode(f.read()).decode('utf8')

data = {
    'unit_test_collection': assignment_url,
    'work_started': "2023-04-12 10:00",
    'work_completed': "2023-04-12 10:01",
    'tests': {
        "dicom_upload": {
            "filename": "test.dcm",
            "encoding": "base64",
            "value": b64_encoded,
        },
    },
}

response = s.post(url, json=data)

# checking the status code to ensure our post succeeded
if response.status_code == 201:
    # this will print out the URL you can use to view your results on the site
    print("Success!")
    print(response.json()['site_url'])
else:
    print("The request failed")
    print(response.json())
