__author__ = 'Alex Berriman <aberriman@formcorp.com.au>'

import formcorp.api

print formcorp.hello()

# FormCorp configurations
public_key = ''
private_key = ''
form_id = 0

# Initialise the module
formcorp.api.init(private_key, public_key)
formcorp.api.use_ssl(False)

# Set the form id
formcorp.api.set_form_id(form_id)

# Fetch the token and shoot off the api call
token = formcorp.api.get_token()