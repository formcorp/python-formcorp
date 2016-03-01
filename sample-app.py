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

# Send a ping
print "Sending ping"
ping = formcorp.api.call('v2/ping/ping?pong=pang', 'GET')
print ping

# Create a user bundle
print "\nCreate a user bundle"
bundle = formcorp.api.call('v2/user/create-bundle', 'POST', {
    "email": "alexb@fishvision.com",
    "password": "Password12!",
    "token": "TEST123"
})
print bundle

# Set the user token
user_token = bundle['response']['data']['token']
print "\nSetting user token to: " + user_token
formcorp.api.set_user_token(user_token)

# Fetch the user messages
print "\nFetching user messages"
messages = formcorp.api.call('v2/messages', 'GET')
print messages

# Fetch the user messages
print "\nFetching latest 2 messages"
messages = formcorp.api.call('v2/messages/index?limit=2', 'GET')
print messages
