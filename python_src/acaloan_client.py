import requests


class AcaLoanClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_event(self, type, uid):
        endpoint = "{}/loan/api/reader".format(self.base_url)
        payload = {"type": type, "uid": uid}
        r = requests.post(endpoint, json=payload)
        print(r.status_code)

        return r.status_code == 200
