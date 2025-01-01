import json

import requests


class Mailing:
    """This is the Mailin client class"""

    def __init__(self, base_url, api_key, timeout=30):
        self.base_url = base_url
        self.api_key = api_key
        if not (0 < timeout <= 60):
            raise ValueError("value not allowed for timeout")

        self.timeout = timeout

    def do_request(self, resource, method, indata):
        url = self.base_url + "/" + resource

        content_type = "application/json"
        headers = {
            "api-key": self.api_key,
            "content-type": content_type,
        }
        try:
            response = requests.request(method.lower(), url, data=indata, headers=headers, timeout=self.timeout)
            return response.json()

        except Exception:
            raise Exception("Request failed")

    def get(self, resource, indata):
        return self.do_request(resource, "GET", indata)

    def post(self, resource, indata):
        return self.do_request(resource, "POST", indata)

    def put(self, resource, indata):
        return self.do_request(resource, "PUT", indata)

    def delete(self, resource, indata):
        return self.do_request(resource, "DELETE", indata)

    def send_transactional_template(self, data):
        id = str(data["id"])
        return self.put("template/" + id, json.dumps(data))

    def send_email(self, data):
        return self.post("smtp/email", json.dumps(data))
