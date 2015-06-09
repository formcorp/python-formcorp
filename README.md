# python-formcorp
A Python framework to integrate with the FormCorp API.

## Sample code:
```python
import formcorp.api

formcorp.api.init(private_key, public_key)
formcorp.api.set_form_id(form_id)

token = formcorp.api.get_token()
try:
    submissions = formcorp.api.call('v1/submissions/ids', "POST", {
        'formId': form_id,
        'token': token
    })
except:
    print "There was an error when attempting to retrieve the form submissions.\n"
    sys.exit()
```
