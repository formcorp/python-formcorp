__author__ = 'Alex Berriman <aberriman@formcorp.com.au>'

import sys
import formcorp.api

# FormCorp configurations
public_key = ''
private_key = ''
form_id = 0

# Initialise the module
formcorp.api.init(private_key, public_key)

# Set the form id
formcorp.api.set_form_id(form_id)

print "======================================================="
print "============= FormCorp Sample Application ============="
print "=======================================================\n"

# Fetch the token and shoot off the api call
print "Retrieving token..."
token = formcorp.api.get_token()
if not token:
    print "Unable to retrieve token from remote API\n"
    sys.exit()

print "Retrieved token: {0}\n".format(token)

# Fetch submissions from the server
print "Retrieving submissions for form..."
try:
    submissions = formcorp.api.call('v1/submissions/ids', "POST", {
        'formId': form_id,
        'token': token
    })
except:
    print "There was an error when attempting to retrieve the form submissions.\n"
    sys.exit()

print "Successfully received {0} submissions.\n".format(len(submissions))

# Retrieve submission data
submission_id = submissions[0]
print "Fetching submission data for id: {0}...".format(submission_id['id'])
submission = formcorp.api.call('v1/submissions/view', "POST", {
    'token': token,
    'id': submission_id,
    'formId': form_id
})

print submission
