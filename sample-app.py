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
formcorp.api.use_ssl(False)
formcorp.api.set_form_id(form_id)

print "======================================================="
print "============= FormCorp Sample Application ============="
print "=======================================================\n"

# Fetch the token and shoot off the api call
print "Retrieving token..."
token = formcorp.api.get_token('v2')
if not token:
    print "Unable to retrieve token from remote API\n"
    sys.exit()

print "Retrieved token: {0}\n".format(token)

formcorp.api.set_token(token)
test = formcorp.api.call('v2/ping/pong', 'GET')

print test