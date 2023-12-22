"""QARepeater is a utility for re-performing QA via the API as a constancy test.

QARepeater can download one or more previously completed sessions for a given
assignment, then use the test values from the completed sessions to re-perform
the test list, and compare the results calculated for the new instances to the
previous results.

Sample Usage:

    import csv
    import qarepeater
    api_key = "your_api_key"
    api_url = "https://staging.radmachine.radformation.com/yourcustomeridentifier/api/"
    assignment_id = 123
    repeater = qarepeater.QARepeater(api_key=api_key, api_url=api_url, assignment_id=assignment_id)
    num_sessions = 1
    results = repeater.repeat_qa(num_sessions)

    with open('results.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for session_result in results:
            writer.writerows(session_result)
            writer.writerow([])


Known Limitations:

    - This could use more work to make it more robust to failures.  API calls
      that fail due to an intermittent issue (connection error, API throttling
      etc) are not handled with a retry and will simply cause the whole attempt
      to fail.  Your script should anticipate and handle exceptions being
      thrown (or better yet, the QARepeater class could be updated to handle
      this better).  For example:

        import time
        ...

        attempts = 0
        results = None
        while attempts < 3:
            attempts += 1
            try:
                results = repeater.repeat_qa(num_sessions)
                break
            except Exception:
                time.sleep(1)

        if results:
            # do something
        else:
            print("Unable to complete QA")

      If you are running e.g. 3 sessions, a failed request may result in 1 or 2
      of the 3 previous sesions being repeated.

    - Upload tests will currently not work due to a bug in the RadMachine API
      (fix scheduled for staging 21 Dec 2023, production 6 Jan 2024.

    - There is no cleanup of performed sessions.  If you want to remove the
      repeated sessions you will need to do so through the web UI.

"""

import base64
import datetime
import io
import json
import time
import urllib
from functools import cached_property
from typing import Any

import requests

CALCULATED_TEST_TYPES = ["composite", "scomposite", "rlookup"]

# throttle your API calls!
API_SLEEP_TIME_S = 0.4
_next_allowed_api_call_time = time.monotonic()


class QARepeater:

    def __init__(self, api_key: str, api_url: str, assignment_id: int):
        self.session = requests.Session()
        self.session.headers.update({"RadAuthorization": f"Token {api_key}"})
        self.root = api_url.strip('/') + '/'
        self.assignment_id = assignment_id
        if not self.root.endswith('/api/'):
            raise ValueError("Invalid API URL. You must provide a URL like https://radmachine.radformation.com/customer/api/")
        try:
            resp = self.get_api_objects('')
            if not isinstance(resp, dict) or 'qa' not in resp:
                raise Exception()
        except Exception:
            raise ValueError("Unable to contact RadMachine. Check your URL and API key are correct.")

    def repeat_qa(self, num_sessions: int = 1) -> list[tuple]:
        """Re-perform one or more of the most recent QA sessions for the given assignment.

        num_sessions: how many QA sessions should be reperformed. Currently
        this is always the most recent sessions although this class could be
        adapted to use specific "baseline" sessions.

        Note: There is a bug in the RadMachine API where previous uploads can
        not be downloaded.  That should be fixed mid Dec 2023 in staging and
        Jan 2024 in production.  For now, upload tests will fail and be
        skipped.
        """
        slug_to_test = {t["slug"]: t for t in self.tests}

        results = []
        # Now we are going to iterate over our last N existing sessions,
        # and use the results form each session to perform the assignment again,
        # and compare the new results to the existing sessions values.
        for previous_session in self.previous_sessions(num_sessions):

            # dictionary mapping test identifer to the previously calculated
            # result for comparing to the new calculated results
            previous_results = self.results_from_session(previous_session)
            previous_calculated_results = {}
            for slug, value in previous_results.items():
                test = slug_to_test[slug]
                if test["type"] in CALCULATED_TEST_TYPES:
                    previous_calculated_results[slug] = value

            # A dictionary of test values to post to the API when performing the new
            # session We add an entry for each test that currently exists in the
            # assigned test list.  To start with we mark each test as being skipped so
            # that if the test list has had new tests added to it since the existing
            # sessions were created, it should still be able to performed using the
            # previous session"s values as input.
            test_values_for_perform = {t["slug"]: {"skipped": True} for t in self.tests if t["type"] not in CALCULATED_TEST_TYPES}
            for slug, value in previous_results.items():
                test = slug_to_test[slug]
                if test["type"] in CALCULATED_TEST_TYPES or value is None:
                    continue

                if test["type"] == "upload":
                    attachment_id = value
                    if attachment_id:
                        # Note this is currently failing because the download link gets redirected
                        # to the RadMachine login page. Should be fixed in staging Mid Dec 2023
                        attachment = self.fetch_attachment(attachment_id)
                        test_values_for_perform[test["slug"]] = {
                            "value": base64.b64decode(attachment.read()).decode(),
                            "filename": attachment.name,
                            "encoding": "base64",
                        }
                else:
                    test_values_for_perform[test["slug"]] = {"value": value }

            new_session = self.perform_session(test_values_for_perform)
            # The structure of results from performing QA is slightly different
            # than that from getting the QA Session directly from the API so we
            # fetch the session we just performed from the API for ease of
            # comparison.
            new_results = self.results_from_session(new_session)
            results.append(self.generate_results_table(previous_session, previous_results, new_session, new_results))

        return results

    def generate_results_table(self, previous_session: dict, previous_results: dict, new_session: dict, new_results: dict) -> list[tuple]:
        table = []
        table.append(["Previous Session Link", previous_session['url']])
        table.append(["Previous Session Date", previous_session['work_completed']])
        table.append(["New Session Link", new_session['url']])
        table.append(["New Session Date", new_session['work_completed']])
        table.append(["Test", "Previous Result", "New Result", "Equal"])
        slug_to_test = {t["slug"]: t for t in self.tests}
        for slug, prev_val in previous_results.items():
            test = slug_to_test[slug]
            new_val = new_results.get(slug, "")
            table.append([test['name'], prev_val, new_val, str(prev_val == new_val)])
        return table

    def get_api_objects(self, path: str, all_pages: bool = True):
        """Fetch arbitrary objects from the API."""
        full_url = urllib.parse.urlunparse(urllib.parse.urlparse(self.root + path.strip('/')))
        return get_api_objects(self.session, full_url, all_pages=all_pages)

    @cached_property
    def assignment(self) -> dict[str, Any]:
        """Return assignment details from RadMachine."""
        return self.get_api_objects(f"/qa/unittestcollections/{self.assignment_id}/")

    @cached_property
    def test_list(self) -> dict[str, Any]:
        """Return test list details from RadMachine.

        We use the `testlist-details` endpoint rather than the default
        `testlists` endpoint because it includes information about all the
        tests which are part of the test list too
        """
        test_list_id = object_id_from_url(self.assignment["tests_object"])
        return self.get_api_objects(f"/qa/testlists-details/{test_list_id}/")

    @cached_property
    def tests(self) -> list[dict[str, Any]]:
        return self.test_list['tests']

    @cached_property
    def unit(self) -> dict[str: Any]:
        """Return unit details from RadMachine."""
        unit_id = object_id_from_url(self.assignment["unit"])
        return self.get_api_objects(f"/units/units/{unit_id}/")

    @cached_property
    def unit_test_infos(self) -> list[dict[str, Any]]:
        """Return a list of all related UnitTestInfo Objects.

        Unit test info is the link between a test and a unit.  Test
        instance results also refer to the unittestinfo rather than the
        unit or test directly.
        """
        # fetch all utis on the unit then filter to those relevant to our test
        # list. This is kinda inefficient but I can't get the API to filter the
        # UnitTestInfo endpoint by test id
        unit_id = object_id_from_url(self.assignment['unit'])
        unit_uti_url = f"/qa/unittestinfos/?unit={unit_id}"
        all_unit_utis = self.get_api_objects(unit_uti_url)
        test_urls = set([t["url"] for t in self.tests])
        test_list_utis = [uti for uti in all_unit_utis if uti['test'] in test_urls]
        return test_list_utis

    def previous_sessions(self, num_previous_instances: int) -> list[dict]:
        url = (
            f"qa/testlistinstances/"
            "?ordering=-work_completed"
            f"&unit_test_collection={self.assignment_id}"
            f"&limit={num_previous_instances}"
        )
        return self.get_api_objects(url, all_pages=False)

    def perform_session(self, tests: dict) -> dict:
        # perform our test list again using the previous session values
        data = {
            "unit_test_collection": self.assignment['url'],
            "work_started": datetime.datetime.now().isoformat(),
            "comment": "Consistency check",
            "tests": tests,
        }
        tli_url = f"{self.root}qa/testlistinstances/"
        response = self.session.post(tli_url, json=data)
        if response.status_code != requests.status_codes.codes.CREATED:
            message = f"{response}"
            try:
                message = f"{message}: {response.json()}"
            except Exception:
                pass
            raise ValueError(f"Failed to repeat session: {message}")
        return self.session.get(response.json()['url']).json()

    def results_from_session(self, qa_session: dict) -> dict[str: Any]:
        """Return a dictionary of { slug: value } for all tests from a session."""
        # set up some mappings to make it easy to look up test info either by API url or slug
        test_url_to_test = {t["url"]: t for t in self.tests}  #

        # Set up a dictionary to map unit test info urls returned from the api to the
        # test they relate to.  This will enble us to map test instance results to the
        # related test below.
        unit_test_info_to_test = {uti["url"]: uti["test"] for uti in self.unit_test_infos}

        results = {}
        for test_instance in qa_session["test_instances"]:
            # each test instance from the session points to a unit test info.
            # we can use that unit test info to see which test was actually performed
            test_url = unit_test_info_to_test[test_instance["unit_test_info"]]
            test = test_url_to_test[test_url]

            # Depending on the test type the value is stored in different fields
            # (e.g. "value" or "string_value") in the test instance result.
            # Use our helper function to get the performed value.
            value = get_testinstance_value(test, test_instance)
            results[test['slug']] = value

        return results

    def fetch_attachment(self, attachment_id: int) -> io.BytesIO:
        """Download an attachment from the API and return it as an io.BytesIO."""
        attachment = self.get_api_objects(f"/attachments/attachments/{attachment_id}/")
        download_link = attachment["download"]
        response = self.session.get(download_link, stream=True)
        f = io.BytesIO(response.raw.read())
        f.name = attachment['label']
        f.seek(0)
        return f


def get_testinstance_value(test, test_instance):
    """Return the test instance result based on the type of test performed."""
    if test_instance["skipped"]:
        return None
    if test["type"] == "simple" and test["statistic"]:
        return json.loads(test_instance["json_value"])
    elif test["type"] in ["boolean", "composite", "constant", "simple", "wraparound"]:
        return test_instance["value"]
    elif test["type"] in ["string", "scomposite", "multchoice", "upload"]:
        return test_instance["string_value"]
    elif test["type"] == "date":
        return test_instance["date_value"]
    elif test["type"] == "datetime":
        return test_instance["datetime_value"]
    elif test["type"] == "ulookup":
        return object_id_from_url(test_instance["unit_lookup_value"])
    elif test["type"] == "rlookup":
        return object_id_from_url(test_instance["unit_lookup_value"])
    else:
        return test_instance["json_value"]

    raise TypeError(f"'{test['type']}' is an unknown test type")


def get_api_objects(session: requests.Session, url: str, all_pages: bool = True) -> dict | list[dict]:
    """Fetch one or more objects from the API.

    If multiple pages are found all pages will be pulled down.
    """
    global _next_allowed_api_call_time
    next_page = url
    results = []
    while next_page:
        now = time.monotonic()
        if now < _next_allowed_api_call_time:
            time.sleep(_next_allowed_api_call_time - now)
        _next_allowed_api_call_time = now + API_SLEEP_TIME_S
        response = session.get(next_page)
        payload = response.json()
        is_single_object = "results" not in payload
        if is_single_object:
            return payload

        results += payload['results']
        next_page = payload.get('next')
        if not (all_pages and next_page):
            break
        time.sleep(1)

    return results


def object_id_from_url(url: str) -> str:
    """Return object id from a url like example.com/customer/api/qa/testlists/123/"."""
    return url.strip("/").rsplit("/")[-1]
