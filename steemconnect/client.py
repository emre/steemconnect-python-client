import json
import urllib.parse

import requests

from .defaults import (OAUTH_BASE_URL, SC2_API_BASE_URL)
from .utils import (requires_access_token, requires_client_id_and_secret)


class Client:

    def __init__(self, client_id=None, client_secret=None, access_token=None,
                 oauth_base_url=None, sc2_api_base_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.oauth_base_url = oauth_base_url or OAUTH_BASE_URL
        self.sc2_api_base_url = sc2_api_base_url or SC2_API_BASE_URL

    @property
    def headers(self):
        return {'Authorization': self.access_token}

    def get_login_url(self, redirect_uri, scope,
                      get_refresh_token=False):
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
        }
        if get_refresh_token:
            params.update({
                "response_type": "code",
            })

        return urllib.parse.urljoin(
            self.oauth_base_url,
            "authorize?" + urllib.parse.urlencode(params))

    @requires_client_id_and_secret
    def get_access_token(self, code):
        post_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        r = requests.post(
            urllib.parse.urljoin(self.sc2_api_base_url, "oauth2/token/"),
            data=post_data
        )

        return r.json()

    @requires_access_token
    def me(self):
        url = urllib.parse.urljoin(self.sc2_api_base_url, "me/")
        r = requests.post(url, headers=self.headers)
        return r.json()

    @requires_access_token
    def broadcast(self, operations):
        url = urllib.parse.urljoin(self.sc2_api_base_url, "broadcast/")
        data = {
            "operations": operations,
        }
        headers = self.headers.copy()
        headers.update({
            "Content-Type": "application/json; charset=utf-8",
        })

        r = requests.post(url, headers=headers, data=json.dumps(data))
        try:
            return r.json()
        except ValueError:
            return r.content


    @requires_client_id_and_secret
    def refresh_access_token(self, refresh_token, scope):
        post_data = {
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope,
        }

        r = requests.post(
            urllib.parse.urljoin(self.sc2_api_base_url, "oauth2/token/"),
            data=post_data
        )

        return r.json()
