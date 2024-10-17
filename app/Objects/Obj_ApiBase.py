import os
import json
from dataclasses import dataclass
from typing import Optional


class Obj_BaseAPIError(Exception):
    pass


@dataclass
class Obj_BaseAPI:
    url: str
    method: str
    data: Optional[dict] = None
    query: Optional[str] = None

    def mount_data(self):
        return {'variables': self.data, 'query': self.query}


class APIs:
    endpoints = json.loads(open(os.path.abspath('data/routes.json'), 'r').read())

    class Login(Obj_BaseAPI):
        def __init__(self, username: str, password: str):
            endpoint = APIs.endpoints['login']

            self.url = endpoint['url']

            self.data = endpoint['data']
            self.data['username'] = username
            self.data['password'] = password

    class Get_All_Accounts(Obj_BaseAPI):
        def __init__(self, userId: str):
            endpoint = APIs.endpoints['get_all_accounts']

            self.url = endpoint['url']
            self.query = endpoint['query']

            self.data = endpoint['data']
            self.data['userId'] = userId

    class Get_All_Contracts(Obj_BaseAPI):
        def __init__(self, partnerNumber: str, profileType: str):
            endpoint = APIs.endpoints['get_all_contracts']

            self.url = endpoint['url']
            self.query = endpoint['query']

            self.data = endpoint['data']
            self.data['partner'] = partnerNumber
            self.data['profileType'] = profileType

    class Get_All_Invoices(Obj_BaseAPI):
        def __init__(self, partner: str, installation: str):
            endpoint = APIs.endpoints['get_all_invoices']

            self.url = endpoint['url']
            self.query = endpoint['query']

            self.data = endpoint['data']
            self.data['partner'] = partner
            self.data['installation'] = installation

    class Get_Invoice(Obj_BaseAPI):
        def __init__(self, contractAccount: str, partner: str,
                     accessId: str, invoiceId: str):
            endpoint = APIs.endpoints['download_invoice']

            self.url = endpoint['url']
            self.query = endpoint['query']

            self.data = endpoint['data']
            self.data['duplicateBillInput']['contractAccount'] = contractAccount
            self.data['duplicateBillInput']['partner'] = partner
            self.data['duplicateBillInput']['accessId'] = accessId
            self.data['duplicateBillInput']['invoiceId'] = invoiceId
