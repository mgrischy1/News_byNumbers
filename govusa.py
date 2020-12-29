import requests


class IRS:

    def __init__(self):
        self.base_url = 'http://catalog.data.gov/api/3/'
        self.headers = {'Content-Type': 'application/json'}

    def request(self, end_point):
        url = f'{self.base_url}{end_point}'
        response = requests.post(url,
                                 headers=self.headers).json()
        print(response)


p = IRS()
p.request('')
