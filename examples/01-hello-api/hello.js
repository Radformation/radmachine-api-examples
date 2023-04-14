/* This example uses the RadMachine API to fetch a list of units from your
 * RadMachine instance and then prints out the name of each unit found.
 * */

import fetch from 'node-fetch';

/* Set your API token and customer identifier here.  As a reminder if you
 * access RadMachine at e.g.  https://radmachine.radformation.com/myclinic/
 * then your customer id is "myclinic"
 */
const token = 'your-token-goes-here';
const customer_id = 'your-customer-id';

const headers = {
  RadAuthorization: `Token ${token}`,
};
fetch(
  `https://radmachine.radformation.com/${customer_id}/api/units/units/`,
  { method: 'GET', headers },
)
  .then((resp) => resp.json())
  .then((payload) => {
    payload.results.forEach((unit) => {
      console.log(unit.name);
    })
  });
