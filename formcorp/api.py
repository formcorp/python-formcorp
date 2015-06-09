from collections import OrderedDict
from hashlib import sha1
import hmac
import httplib
import json
import random
import string
import time
import urllib

"""
API configuration.
"""
API_HOSTNAME = 'api.formcorp.local'

# Module constants
_constants = {
    'SIGNATURE_ENCODING': "utf-8",
    'REQUEST_TYPE_POST': 'POST',
    'REQUEST_TYPE_GET': 'GET',
    'REQUEST_TYPE_PUT': 'PUT',
    'HEADER_PARAM_AUTHORIZATION': 'Authorization',
    'HEADER_PARAM_SIGNATURE': 'Signature',
    'HEADER_PARAM_ACCEPT': 'Accept',
    'HEADER_PARAM_BEARER': 'Bearer {0}',
    'HEADER_APPLICATION_JSON': 'application/json',
    'HEADER_PARAM_CONTENT_TYPE': 'Content-type',
    'HEADER_URL_FORM_ENCODED_TYPE': 'application/x-www-form-urlencoded'
}

# Configuration client can alter
_config = dict(private_key=None, public_key=None, form_id=None, use_ssl=False)


def init(private_key, public_key):
    """
    Initialise the module.

    :type private_key: basestring
    :type public_key: basestring
    """
    assert isinstance(private_key, basestring)
    assert isinstance(public_key, basestring)

    global _config

    _config['private_key'] = private_key
    _config['public_key'] = public_key


def use_ssl(ssl=True):
    """
    Whether to use SSL when communicating with the remote API
    :type ssl: boolean
    """
    _config['use_ssl'] = ssl


def set_form_id(form_id):
    """
    Set the form id
    :type form_id: int
    """
    assert isinstance(form_id, int)
    _config['form_id'] = form_id


def call(uri, request_method=None, data=None, headers=None):
    """
    Shoot off a call to the remote API.
    :param uri:
    :param request_method:
    :param data:
    :param headers:
    :return:
    """
    # Set default values
    if request_method is None:
        request_method = _constants['REQUEST_TYPE_POST']

    if data is None:
        data = {}

    if headers is None:
        headers = {}

    # Check to make sure first character is a forward slash
    if uri[0:1] != '/':
        uri = '/' + uri

    # Set base headers
    headers[_constants['HEADER_PARAM_AUTHORIZATION']] = _constants['HEADER_PARAM_BEARER'].format(_config['public_key'])
    headers[_constants['HEADER_PARAM_SIGNATURE']] = _generate_signature(request_method, uri, data)
    headers[_constants['HEADER_PARAM_ACCEPT']] = _constants['HEADER_APPLICATION_JSON']

    # Initialise the connection
    if _config['use_ssl']:
        connection = httplib.HTTPSConnection(API_HOSTNAME)
    else:
        connection = httplib.HTTPConnection(API_HOSTNAME)

    if request_method.upper() == _constants['REQUEST_TYPE_POST']:
        # Send a POST request
        headers[_constants['HEADER_PARAM_CONTENT_TYPE']] = _constants['HEADER_URL_FORM_ENCODED_TYPE']
        connection.request(_constants['REQUEST_TYPE_POST'], uri, urllib.urlencode(data), headers)
    elif request_method.upper() == _constants['REQUEST_TYPE_GET']:
        # Send a GET request
        connection.request(_constants['REQUEST_TYPE_GET'], uri, headers)

    # Retrieve the results of the request
    result = connection.getresponse()

    # Ensure a valid response was received from the server
    if result.status != 200:
        raise Exception("Unable to connect to remote API")

    # Attempt to decode json result
    res = result.read()
    try:
        data = json.loads(res)
    except ValueError:
        raise Exception("Unable to decode server result")

    return data


def get_token():
    """
    Retrieve a token from the server.
    :return: string
    """
    if not _initialised():
        return False

    post_data = {
        'timestamp': int(time.time()),
        'nonce': _generate_nonce()
    }

    result = call('v1/auth/token', 'POST', post_data)

    # Attempt to return the result from the server
    try:
        return result['token']
    except KeyError:
        return False


def _initialised():
    """
    Checks to see if the API has been properly initialised
    :return: boolean
    """
    global _config

    try:
        assert isinstance(_config['private_key'], basestring)
        assert isinstance(_config['public_key'], basestring)
        assert isinstance(_config['form_id'], int)

        return True
    except AssertionError:
        return False


def _generate_nonce(length=40):
    """
    Generates a random nonce string
    :type length: int
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def _api_url():
    """
    Generates a signature to use to uniquely identify the request
    :return: string
    """
    url = "http"
    if _config["use_ssl"]:
        url += "s"

    url += '://{0}'.format(API_HOSTNAME)


def _generate_signature(request_method, uri, data=None):
    """
    Generate a signature to send with the request.
    :param request_method: string
    :param uri: string
    :param data: dict
    :return: string
    """
    if data is None:
        data = {}

    # Typecast each dictionary object to string
    if len(data) > 0:
        for attr, value in data.iteritems():
            data[attr] = str(value)

    # Create an ordered dict (python sorts by key hashes, need to sort in order elements were added)
    obj = OrderedDict()
    obj['method'] = request_method.upper()
    obj['uri'] = uri
    obj['data'] = data
    plaintext = json.dumps(obj)

    # Encode the string
    encoded = unicode(plaintext, _constants['SIGNATURE_ENCODING'])

    # Hash the signature
    hashed = hmac.new(_config['private_key'], encoded, sha1)
    hash = hashed.digest().encode("base64").rstrip('\n')

    return hash
