""" Base Process Maker module """
import os
import urllib.parse
import requests



class ProcessMaker:
    """ Base Process Maker class """

    token = None

    def init(self, workspace):
        """ initialize accela """
        self.load_token(workspace)

    def load_token(self, workspace):
        """ get token """

        username = os.environ.get('PM_USERNAME')
        password = os.environ.get('PM_PASSWORD')
        scope = os.environ.get('PM_SCOPE')

        self.token = self.get_token(username, password, scope, workspace)


    @staticmethod
    def get_token(username, password, scope, workspace):
        """
        | Get authentication token
        """
        params = {}
        params['grant_type'] = 'password'
        params['client_id'] = os.environ.get('CLIENT_ID')
        params['client_secret'] = os.environ.get('CLIENT_SECRET')
        params['username'] = username
        params['password'] = password
        params['scope'] = scope

        url = os.environ.get('PM_SERVER')
        url = urllib.parse.urljoin(url, workspace+'/oauth2/token')
        content_json = False

        headers = {}
        response = requests.post(url, headers=headers, data=params)

        if response.status_code == 200:
            content_json = response.json()
        else:
            raise ValueError('get_token.request('+ str(response.status_code) +'):'+response.text)

        return content_json

    def post(self, path, json=None):
        """
        | POST request to path
        """
        data = None
        content_json = {}

        url = os.environ.get('PM_SERVER')
        url = urllib.parse.urljoin(url, path)

        headers = {}
        if self.token and "access_token" in self.token:
            headers['Authorization'] = 'Bearer '+ self.token['access_token']
        if json:
            headers['Content-Type'] = 'application/json'
            data = json

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            content_json = response.json()
        else:
            raise ValueError('get_token.request('+ str(response.status_code) +'):'+response.text)

        return content_json
