client_id = 'py-client'
client_secret = 'py-secret'
scope = 'openid email profile'
discovery_endpoint = 'https://localhost:8443/.well-known/openid-configuration'

# set the environment CURL_CA_BUNDLE=
# to ignore certificate errors

OAUTH_CREDENTIALS = {
    'CA': {
        'id': client_id,
        'secret': client_secret,
        'discovery_endpoint': discovery_endpoint,
        'scope': scope
    }
}
