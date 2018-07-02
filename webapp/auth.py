from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service

import urllib.request as urllib2
import json


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.discovery_endpoint = credentials['discovery_endpoint']
        self.scope = credentials['scope']

    def authorise(self, nextpage):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class CASignIn(OAuthSignIn):

    def __init__(self):

        super(CASignIn, self).__init__('CA')
        self.next_page = None
        cainfo = urllib2.urlopen(self.discovery_endpoint)
        ca_params = json.load(cainfo)
        self.service = OAuth2Service(
            name='CA',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=ca_params.get('authorization_endpoint'),
            base_url=ca_params.get('userinfo_endpoint'),
            access_token_url=ca_params.get('token_endpoint')
        )

    def authorise(self, next_page):
        self.next_page = next_page
        return redirect(self.service.get_authorize_url(
            scope=self.scope,
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):

        # Check if cancelled or invalid UID / password
        error = request.args.get('error')
        if error:
            return None, None, None, None, None, None, error, request.args.get("error_description")

        if 'code' not in request.args:
            return None, None, None, None, None, None

        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()
                  },
            decoder=json.loads
        )

        me = oauth_session.get('').json()
        return self.next_page, me['name'], me['email'], \
               me['family_name'], me['nickname'], me['preferred_username'], None, None
